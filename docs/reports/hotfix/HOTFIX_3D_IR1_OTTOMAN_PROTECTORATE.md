# HOTFIX-3D - Protectorat ottoman IR1 / Mamluk Iraq

## 1. Résumé

Cette phase importe uniquement la relation diplomatique de sujet entre l'Empire ottoman et `IR1` / Mamluk Iraq. Le pacte ajouté fait de `IR1` un protectorat de `TUR`, conformément au hotfix upstream.

## 2. Pourquoi cette phase est limitée à la relation TUR -> IR1

HOTFIX-3A a créé le tag IR1, HOTFIX-3B l'a activé territorialement, et HOTFIX-3C lui a donné une armée terrestre minimale. Cette phase ajoute seulement le lien diplomatique nécessaire avec l'Empire ottoman, sans importer la guerre, les objectifs IA, les relations régionales avec `PER`, `ARB` ou `OMA`, ni d'autres changements du hotfix.

## 3. Fichier hotfix consulté

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\diplomacy\00_subject_relationships.txt`

## 4. Fichiers modifiés

- `common/history/diplomacy/00_subject_relationships.txt`
- `docs/reports/hotfix/HOTFIX_3D_IR1_OTTOMAN_PROTECTORATE.md`

## 5. Relation importée

| Élément | Valeur |
|---|---|
| Suzerain | `c:TUR` |
| Sujet | `c:IR1` |
| Type | `protectorate` |
| Syntaxe | `create_diplomatic_pact = { country = c:IR1 type = protectorate }` dans le bloc `c:TUR ?= { ... }` |

Justification : le hotfix ajoute exactement ce pacte en tête du bloc ottoman. Le type `protectorate` est déjà utilisé dans le fichier local et dans les fichiers vanilla 1.13, donc il est compatible avec le style existant.

## 6. Compatibilité avec gov_pashalik

Le gouvernement `gov_pashalik` exige :

- `has_law = law_type:law_monarchy`
- `exists = c:IR1`
- `exists = c:TUR`
- `c:IR1 ?= ROOT`
- `is_subject_of = c:TUR`
- ne pas être `subject_type_crown_land`

Après cette phase :

- `IR1` existe via HOTFIX-3A.
- `TUR` existe déjà dans le mod.
- `IR1` a `law_monarchy` dans `common/history/countries/ir1 - mamluk iraq.txt`.
- `IR1` est maintenant sujet de `TUR` via `type = protectorate`.
- `protectorate` n'est pas `subject_type_crown_land`.

La relation importée rend donc les conditions de `gov_pashalik` cohérentes sans modifier le fichier de gouvernement.

## 7. Ce qui n'a pas été importé

- Aucun diplomatic play `PER / IR1 / ARB / OMA`.
- Aucune guerre initiale.
- Aucune relation diplomatique `PER`, `ARB` ou `OMA`.
- Aucun secret goal IA.
- Aucun changement aux states, pops, bâtiments ou formations militaires.
- Aucun changement aux pays, localisations, événements ou map_data.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Aucun changement aux lois HOTFIX-2.

## 8. Vérifications effectuées

Commandes et recherches effectuées :

- `git status --short`
- `git branch --show-current`
- `git log --oneline -5`
- `git stash list`
- comparaison ciblée fork/hotfix de `00_subject_relationships.txt`
- recherche `c:IR1`, `c:TUR`, `protectorate`, `subject_type`
- vérification des conditions de `gov_pashalik`

Résultat :

- Aucun doublon `c:TUR -> c:IR1` n'existait avant l'ajout.
- Le seul ajout gameplay est le pacte protectorat `TUR -> IR1`.
- `gov_pashalik` n'a pas été modifié.

## 9. Risques restants

- Le rapport de force diplomatique exact entre `TUR` et `IR1` doit être testé en jeu.
- Aucun diplomatic play historique n'est encore importé, donc les tensions `PER / IR1 / ARB / OMA` du hotfix restent absentes.
- Il faudra vérifier que l'interface affiche bien IR1 comme protectorat ottoman et non comme sujet d'un autre type.

## 10. Tests à faire en jeu

1. Lancer le mod seul.
2. Démarrer une partie en 1776.
3. Vérifier que `IR1` existe sur Basra, Baghdad, Mosul et Deir ez-Zor.
4. Vérifier que `IR1` est protectorat/sujet de `TUR`.
5. Vérifier que le gouvernement affiché pour IR1 est cohérent avec `gov_pashalik`.
6. Observer un mois de jeu.
7. Surveiller `error.log` avec les motifs `IR1`, `protectorate`, `subject`, `gov_pashalik`, `create_diplomatic_pact`.

## 11. Liste exacte des fichiers modifiés

- `common/history/diplomacy/00_subject_relationships.txt`
- `docs/reports/hotfix/HOTFIX_3D_IR1_OTTOMAN_PROTECTORATE.md`

## 12. Confirmation de périmètre

- Aucun diplomatic play importé.
- Aucune guerre importée.
- Aucune relation `PER`, `ARB` ou `OMA` modifiée.
- Aucun state modifié.
- Aucune pop modifiée.
- Aucun bâtiment modifié.
- Aucune formation militaire modifiée.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Le stash MARATH n'a pas été appliqué ni modifié.
