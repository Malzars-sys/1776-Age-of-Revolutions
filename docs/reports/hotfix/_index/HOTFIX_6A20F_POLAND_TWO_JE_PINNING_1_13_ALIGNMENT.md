# HOTFIX-6A.20F — Alignement 1.13 des deux pinning Pologne

Date : 4 août 2026
Branche : `hotfix-dlc-audit`
HEAD d’entrée : `4edafc4549624d77c09f7adb313eccd3b02005d3`
Message : `Audit Poland journal entry pinning for 1.13`

## 1. Résultat

Les deux propriétés de pinning obsolètes de
`common/journal_entries/00_poland.txt` ont été remplacées par leur forme
Victoria 3 1.13. La correction modifie exactement deux lignes dans deux objets
et aucun autre octet gameplay.

Le résultat statique atteint le hash théorique de 6A.20. Aucun runtime n’a été
lancé. Les deux diagnostics présents dans les logs existants restent une
baseline historique antérieure à la correction ; leur passage de `2 → 0`
doit être mesuré dans une nouvelle génération par la phase humaine distincte
`HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_QA`.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| racine Git | dépôt attendu |
| branche | `hotfix-dlc-audit` |
| HEAD | `4edafc4` |
| message HEAD | `Audit Poland journal entry pinning for 1.13` |
| rapport 6A.20 dans HEAD | présent avec tous les verdicts requis |
| arbre suivi avant correction | propre |
| index Git | vide |
| `git diff --check` | propre |
| Victoria 3 / Dowser / launcher Paradox | aucun processus |
| stash NAVY-3C-3 | `518df704fa14599c0f254fae13859210663dd976`, intact |
| non-suivis | uniquement les huit éléments protégés connus |

Les non-suivis protégés n’ont pas été ouverts, modifiés, déplacés ou indexés.

## 3. État byte-level avant correction

| Propriété | Valeur |
| --- | --- |
| fichier | `common/journal_entries/00_poland.txt` |
| encodage | UTF-8 avec BOM |
| fins de ligne | LF, 132 séparateurs |
| lignes | 132 |
| taille | 2 972 octets |
| SHA-256 | `DD2696FACF3D7988A933E7541D00D989E3E4B813574493D28A2BCA7AA1DACFD0` |
| ancienne propriété | 2 occurrences |
| nouvelle propriété | 0 occurrence |

Les deux occurrences appartenaient exclusivement à :

- `je_christ_of_nations`, ligne 59 ;
- `je_poland_lithuania`, ligne 131.

## 4. Méthode et diff

Un patch minimal a remplacé les deux séquences ASCII exactes sans sérialiseur,
reformatage ni normalisation des fins de ligne. Les octets, le BOM, les LF et
les lignes ont été recomptés immédiatement après écriture.

```diff
@@ je_christ_of_nations, ligne 59 @@
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes

@@ je_poland_lithuania, ligne 131 @@
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
```

Le diff gameplay est exactement `2+/2-` dans un seul fichier.

## 5. État byte-level après correction

| Propriété | Valeur |
| --- | --- |
| encodage | UTF-8 avec BOM, inchangé |
| fins de ligne | LF, 132 séparateurs, inchangé |
| lignes | 132 |
| taille | 3 016 octets |
| SHA-256 | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` |
| ancienne propriété | 0 occurrence |
| nouvelle propriété | 2 occurrences |

Le remplacement inverse, calculé en mémoire sur les deux nouvelles séquences,
reconstitue exactement :

```text
DD2696FACF3D7988A933E7541D00D989E3E4B813574493D28A2BCA7AA1DACFD0
```

Cette identité inverse prouve que tous les autres octets sont inchangés.

## 6. Inspection fonctionnelle

### `je_christ_of_nations`

Le hash inverse et la relecture confirment l’invariance de :

- l’icône et `je_group_poland` ;
- la visibilité lobby pour POL ou KRA ;
- `christ_of_nations_button` ;
- les conditions POL, KRA, GAL, souverain et culture polonaise ;
- le bloc géographique fork fondé sur `sr:region_poland` ;
- la technologie `nationalism` ;
- le scope `polish_culture_scope` ;
- la complétion territoriale du fork ;
- l’événement final `poland_events.4`.

### `je_poland_lithuania`

Le hash inverse et la relecture confirment l’invariance de :

- l’icône et `je_group_poland` ;
- l’absence de bloc `is_shown_in_lobby` propre au fork ;
- la condition de culture primaire polonaise ;
- `pan-nationalism`, le contexte PLC et le tooltip ;
- l’événement d’entrée `poland_events.6` ;
- Minsk, Kiev et les sept états homeland requis ;
- `greater_commonwealth_var` et `poland_events.7` ;
- les homelands de Vilnius, Brest et Volhynie ;
- les cultures ukrainienne et biélorusse ;
- tous les loyalistes et tooltips finaux.

Aucun hunk de la source ou de la vanilla n’a été importé. Géographie,
visibilité, complétion, progression, récompenses, effets, scopes, cultures,
technologies, événements, boutons et formation de la Pologne-Lituanie restent
strictement ceux du fork d’entrée.

## 7. Fichier custom et protections

`common/journal_entries/07_poland_lithuania_mod.txt` est inchangé par rapport
au HEAD ; son SHA-256 reste
`5D3EFE884DE36B6B379FCE1A81D3DC39979DA137D329BD5B4B1D7F9ACC13B1C5`.

Égypte, intérêts déclarés, DEI/VOC, HBC/Navigation Acts, Coup, Imperialism,
Tanzimat, Merchant Banking, NAVY, ADMIN, MARATH/SAT/KHP, BIC, GBR, Inde,
Japon, Mamluk Iraq, Amérique, France, technologies, localisations, sauvegardes
et descripteurs restent fermés et inchangés.

La loi BIC `law_frontier_colonization` n’a pas été touchée et
`law_colonial_exploitation` n’a pas été restaurée.

## 8. Baseline des logs et runtime ultérieur

Les logs n’ont pas été modifiés et aucune nouvelle génération n’a été produite.
La baseline historique avant nouveau runtime reste :

```text
Unexpected token: should_be_pinned_by_default
common/journal_entries/00_poland.txt
lignes 59 et 131
2 diagnostics dédupliqués dans debug.log
```

6A.20Q devra effectuer une seule ouverture humaine :

1. confirmer le fork exact et lancer une partie neuve 1776 ;
2. ne forcer aucune journal entry ;
3. produire une nouvelle génération de logs ;
4. fermer Victoria 3 et le launcher ;
5. confirmer les diagnostics ciblés `2 → 0` ;
6. confirmer l’absence de nouvelle erreur attribuable à `00_poland.txt` ;
7. ne pas prétendre valider le comportement UI si les entrées ne sont pas
   naturellement visibles.

Cette QA n’a pas été commencée.

## 9. Fichiers modifiés

Gameplay :

- `common/journal_entries/00_poland.txt` — deux substitutions seulement.

Documentation autorisée :

- création de `HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_ALIGNMENT.md` ;
- mise à jour de `docs/reports/hotfix/INDEX.md` ;
- mise à jour de `HOTFIX_REPORT_INDEX.csv` ;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- mise à jour de `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- mise à jour de l’unique ligne Pologne dans
  `HOTFIX_MERGE_REMAINING_WORK.csv` ;
- mise à jour de `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 10. Validation

`git diff --check` est propre, l’index Git reste vide, le HEAD reste
`4edafc4`, le stash est intact et aucun commit automatique n’a été créé.
Exactement un fichier gameplay est modifié avec un diff `2+/2-`. Aucun
runtime n’a été exécuté.

```text
HOTFIX_6A20F_POLAND_TWO_JE_PINNING_1_13_STATIC_PASS
POLAND_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_APPLIED
POLAND_TWO_JE_PINNING_OLD_PROPERTIES_2_TO_0
POLAND_TWO_JE_PINNING_NEW_PROPERTIES_0_TO_2
POLAND_TWO_JE_PINNING_GAMEPLAY_DIFF_2_PLUS_2_MINUS
POLAND_TWO_JE_PINNING_SHA256_MATCH
POLAND_TWO_JE_PINNING_OTHER_BYTES_UNCHANGED
POLAND_GEOGRAPHY_VISIBILITY_COMPLETION_AND_EFFECTS_UNCHANGED
POLAND_CUSTOM_JOURNAL_ENTRY_FILE_UNCHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_QA
```
