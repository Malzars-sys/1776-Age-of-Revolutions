# HOTFIX-6A.20 — Audit de l’alignement 1.13 des journal entries polonaises

Date : 4 août 2026
Branche : `hotfix-dlc-audit`
HEAD d’entrée : `4cc3e519c71cdd1f4fdde8faad0b613e729486fd`
Message : `Reindex residual global scripts after 6A18`

## 1. Verdict

L’audit statique et documentaire des deux propriétés de pinning est terminé.
Les deux diagnostics courants correspondent exactement aux deux anciennes
propriétés. La source hotfix et la vanilla 1.13 convergent exactement sur la
nouvelle propriété dans les mêmes objets et à la même position structurelle.

Un correctif théorique limité à un fichier, deux objets et deux hunks est
reproductible. Il n’absorbe aucune différence de géographie, visibilité,
complétion, progression, récompense ou effet. La phase corrective
`HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT` est sélectionnée, mais
n’est pas commencée.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| racine Git | dépôt attendu |
| branche | `hotfix-dlc-audit` |
| HEAD | `4cc3e51` |
| message HEAD | `Reindex residual global scripts after 6A18` |
| rapport 6A.19 dans HEAD | présent avec tous les verdicts requis |
| arbre suivi | propre |
| index Git | vide |
| `git diff --check` | propre |
| processus Victoria 3 / Dowser / launcher Paradox | aucun |
| stash NAVY-3C-3 | `518df704fa14599c0f254fae13859210663dd976`, intact |
| non-suivis | uniquement les huit éléments protégés connus |
| runtime 6A.20 | aucun |

Ni `bject` ni les sept fichiers de recherche technologique n’ont été ouverts
ou modifiés.

## 3. Périmètre et hashes

Seul `common/journal_entries/00_poland.txt` a été lu côté gameplay. Les deux
objets audités sont `je_christ_of_nations` et `je_poland_lithuania`.
`07_poland_lithuania_mod.txt` reste hors périmètre.

| Arbre | octets | lignes | SHA-256 |
| --- | ---: | ---: | --- |
| fork | 2 972 | 132 | `DD2696FACF3D7988A933E7541D00D989E3E4B813574493D28A2BCA7AA1DACFD0` |
| source hotfix | 2 978 | 130 | `9B01C5DBFA033492753278F044DC20BF3C1F1AC8701C95E6AEA51C82B65B930F` |
| vanilla 1.13 | 3 125 | 136 | `8BF208D5A89595E76131B69D30BD3DE26ECC92A76F623D3040CBC11349B76A78` |

Les trois hashes correspondent exactement aux références 6A.19. Le hash du
fork est encore identique après toutes les lectures.

## 4. Diagnostics existants

Clé de déduplication :

```text
génération + message normalisé + chemin + ligne
```

Message exact normalisé :

```text
Unexpected token: should_be_pinned_by_default
```

Chemin :

```text
common/journal_entries/00_poland.txt
```

| Génération | horodatage du log | brut | dédupliqué | lignes |
| --- | --- | ---: | ---: | --- |
| `debug.log` | 2026-08-04 19:43:32 | 2 | 2 | 59 ; 131 |
| `debug.3.log` | 2026-08-04 19:27:30 | 2 | 2 | 59 ; 131 |
| `debug.5.log` | 2026-08-04 19:08:14 | 2 | 2 | 59 ; 131 |
| `debug.1.log`, `debug.2.log`, `debug.4.log` | rotations disponibles | 0 | 0 | aucune |
| `error*.log`, `game*.log` | générations disponibles | 0 | 0 | aucune |

Dans `debug.log`, les deux occurrences portent l’horodatage interne
`19:38:06`. Les logs ne nomment pas les objets ; l’attribution est faite par
les lignes et les limites complètes des objets : ligne 59 dans
`je_christ_of_nations`, ligne 131 dans `je_poland_lithuania`.

## 5. Propriété de pinning 1.13

La recherche dans `game/common/journal_entries` donne :

- 394 occurrences de
  `should_be_pinned_by_default_uninvolved_or_context` dans 157 fichiers ;
- zéro occurrence de `should_be_pinned_by_default =` ;
- des valeurs `yes` et `no` dans des objets aux triggers et géographies
  variés ;
- deux occurrences de la nouvelle propriété dans le fichier vanilla Pologne,
  une dans chacun des objets audités.

Ces scripts vanilla et l’absence de rejet de la nouvelle forme démontrent que
la propriété est acceptée pour les journal entries 1.13. Les six diagnostics
observés sur trois générations démontrent inversement que l’ancienne propriété
est rejetée dans le fork courant.

La nouvelle propriété est un champ de premier niveau de la journal entry dans
la source et la vanilla. Elle ne se trouve dans aucun scope de visibilité,
géographie ou complétion et ne dépend d’aucun champ adjacent. Son nom indique
un comportement de pinning selon implication ou contexte ; aucune sémantique
plus précise n’est affirmée sans documentation moteur.

## 6. Comparaison fonctionnelle — `je_christ_of_nations`

Bornes : fork lignes 1–60, source 1–51, vanilla 1–59.

| Groupe | fork | source | vanilla | relation | fonction / setup 1776 | correction future |
| --- | --- | --- | --- | --- | --- | --- |
| pinning | ancienne propriété, ligne 59 | nouvelle propriété | nouvelle propriété | source = vanilla ≠ fork | propriété UI de premier niveau, syntaxe fork rejetée | **incluse** |
| icône, groupe | identiques | identiques | identiques | trois égaux | présentation | exclue, inchangée |
| visibilité lobby | POL ou KRA | identique | identique | trois égaux | accès lobby | exclue, inchangée |
| bouton scripté | `christ_of_nations_button` | identique | identique | trois égaux | action UI | exclue, inchangée |
| visibilité inactive — pays/culture | POL, KRA ou souverain GAL polonais | identique | identique | trois égaux | admissibilité pays | exclue, inchangée |
| visibilité inactive — géographie | `NOT sr:region_poland/any_scope_state` | absente | `NOT any_scope_state/is_in_geographic_region` | trois voies divergentes | préservation du setup géographique du fork ; intention non tranchée | **exclue** |
| création possible | technologie `nationalism` | identique | identique | trois égaux | activation technologique | exclue, inchangée |
| immédiat | sauvegarde du scope culture polonaise | identique | identique | trois égaux | scope événementiel | exclue, inchangée |
| complétion | tous les états de `sr:region_poland` au root | `any_state_in_poland_old` | états du `geographic_region_poland_old` | trois voies divergentes | condition territoriale ; géographie 1776 non arbitrée | **exclue** |
| effet final | `poland_events.4` | identique | identique | trois égaux | événement de fin | exclue, inchangée |
| échec / progression / récompense séparée | absents | absents | absents | trois égaux | aucun groupe autonome | aucune modification |

## 7. Comparaison fonctionnelle — `je_poland_lithuania`

Bornes : fork lignes 62–132, source 53–130, vanilla 61–136.

| Groupe | fork | source | vanilla | relation | fonction / setup 1776 | correction future |
| --- | --- | --- | --- | --- | --- | --- |
| pinning | ancienne propriété, ligne 131 | nouvelle propriété | nouvelle propriété | source = vanilla ≠ fork | propriété UI de premier niveau, syntaxe fork rejetée | **incluse** |
| icône, groupe | identiques | identiques | identiques | trois égaux | présentation | exclue, inchangée |
| visibilité lobby | absente | région Pologne + culture primaire polonaise | culture primaire polonaise | trois voies divergentes | accès lobby ; comportement fork à préserver | **exclue** |
| visibilité inactive | culture primaire polonaise | région Pologne + culture polonaise | culture polonaise | fork = vanilla ≠ source | admissibilité pays | **exclue** |
| création possible | `pan-nationalism`, tooltip et PLC | identique | identique | trois égaux | activation et contexte PLC | exclue, inchangée |
| immédiat | `poland_events.6` | identique | identique | trois égaux | événement d’entrée | exclue, inchangée |
| complétion | Minsk, Kiev et sept états homeland | identique | identique | trois égaux | condition territoriale | exclue, inchangée |
| effets finaux / récompenses | variable Commonwealth, événement 7, homelands, cultures et loyalistes | identiques | identiques | trois égaux | formation et récompenses | exclues, inchangées |
| échec / progression | absents | absents | absents | trois égaux | aucun groupe autonome | aucune modification |

## 8. Patch théorique

Le fichier est UTF-8 avec BOM. Le remplacement exact a été calculé en mémoire,
sans fichier temporaire et sans écriture gameplay.

```diff
@@ je_christ_of_nations, ligne 59 @@
     }

-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }

@@ je_poland_lithuania, ligne 131 @@
     }

-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }
```

Résultat théorique :

| Mesure | Valeur |
| --- | --- |
| substitutions | 2 |
| lignes ajoutées | 2 |
| lignes supprimées | 2 |
| lignes totales | 132, inchangé |
| octets | 3 016, soit +44 |
| SHA-256 théorique | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` |
| autres lignes modifiées | 0 |

Les conditions géographiques, scopes pays, visibilité, complétion,
progression, récompenses, effets et propriétés UI adjacentes restent
strictement ceux du fork.

## 9. Réponses aux neuf questions

1. **Oui.** Les deux diagnostics actuels pointent exactement les deux anciennes
   propriétés aux lignes 59 et 131.
2. **Oui.** Source et vanilla emploient exactement la nouvelle propriété avec
   la valeur `yes` dans chacun des deux objets.
3. **Oui, statiquement.** La propriété est au niveau racine de chaque journal
   entry, comme dans la source, la vanilla Pologne et 157 fichiers vanilla.
4. **Oui.** Les substitutions ne traversent aucun bloc géographique et ne
   changent aucun scope.
5. **Oui.** Le correctif est limité à un fichier, deux objets et deux hunks.
6. **Oui.** Aucun trigger, région, visibilité, progression, récompense ou effet
   adjacent ne doit être absorbé.
7. **Oui.** La correction syntaxique peut être sélectionnée sans décision de
   design ; les divergences fonctionnelles restent hors périmètre.
8. **Oui, après correction.** Un lancement ciblé est recommandé pour confirmer
   le chargement et le passage des deux diagnostics de 2 à 0. Il n’est pas
   requis pour le présent audit.
9. **Oui pour le parsing des deux définitions, sans forçage.** Leur chargement
   est global et les deux erreurs sont individualisées par ligne. En revanche,
   un lancement ne devra pas prétendre valider le comportement UI de pinning
   des deux entrées si aucune nation naturellement éligible ne les expose en
   1776 ; aucune chaîne ne devra être forcée pour fabriquer cette preuve.

## 10. Conditions de sélection

Toutes les conditions de sélection de 6A.20F sont satisfaites :

- deux anciennes clés présentes et deux diagnostics courants correspondants ;
- deux nouvelles clés présentes dans la source et dans la vanilla ;
- propriété 1.13 valide au niveau racine des deux objets ;
- deux hunks indépendants et hash théorique reproductible ;
- aucune modification géographique, de visibilité, de complétion ou d’effet ;
- aucune collision protégée ;
- validation statique future : hash, diff `2+/2-`, deux anciennes occurrences
  à zéro, deux nouvelles occurrences et invariance des autres lignes ;
- validation runtime future : un lancement minimal, sans forçage, avec
  déduplication du chemin et confirmation des diagnostics `2 → 0`.

La phase sélectionnée est exclusivement :

`HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT`

Elle n’a pas été commencée.

## 11. Protections et fichiers

`07_poland_lithuania_mod.txt`, Égypte, intérêts déclarés, DEI/VOC,
HBC/Navigation Acts, Coup, Imperialism, Tanzimat, Merchant Banking, NAVY,
ADMIN, MARATH/SAT/KHP, BIC, GBR, Inde, Japon, Mamluk Iraq, Amérique, France,
technologies, localisations, sauvegardes et descripteurs restent inchangés et
fermés.

La loi BIC `law_frontier_colonization` n’a pas été touchée et
`law_colonial_exploitation` n’a pas été restaurée.

Seuls les livrables documentaires autorisés de 6A.20 sont modifiés. Aucun
fichier gameplay n’a changé, aucun runtime n’a été lancé et aucun commit n’a
été créé.

```text
HOTFIX_6A20_POLAND_JOURNAL_ENTRY_1_13_ALIGNMENT_AUDIT_COMPLETE
POLAND_TWO_JE_THREE_WAY_COMPARISON_COMPLETE
POLAND_TWO_JE_PINNING_DIAGNOSTICS_CONFIRMED
POLAND_PINNING_AND_GEOGRAPHIC_HUNKS_SEPARATED
POLAND_TWO_HUNK_THEORETICAL_PATCH_COMPUTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
POLAND_TWO_JE_PINNING_ATOMIC_ALIGNMENT_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT
```
