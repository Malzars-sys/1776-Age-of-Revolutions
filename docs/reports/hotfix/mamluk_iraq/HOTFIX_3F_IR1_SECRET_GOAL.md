# HOTFIX-3F - Secret goal IA IR1 / Mamluk Iraq

## 1. Résumé

Cette phase importe uniquement l'objectif IA caché `IR1 -> TUR` depuis le hotfix upstream. L'objectif ajouté pousse l'Irak mamelouk à défier son suzerain ottoman via `secret_goal = defy`.

## 2. Pourquoi cette phase est limitée au secret goal IR1

Les phases précédentes ont déjà importé le tag IR1, son territoire, son armée, son protectorat ottoman et le diplomatic play régional. Cette phase ne doit ajouter que le comportement IA minimal correspondant, sans modifier la diplomatie, le diplomatic play, les states, les pops, les bâtiments ou les formations militaires.

## 3. Fichier hotfix consulté

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\ai\00_secret_goals.txt`

## 4. Fichiers modifiés

- `common/history/ai/00_secret_goals.txt`
- `docs/reports/hotfix/HOTFIX_3F_IR1_SECRET_GOAL.md`

## 5. Secret goal importé

| Élément | Valeur |
|---|---|
| Pays source | `c:IR1` |
| Pays cible | `c:TUR` |
| Objectif | `defy` |
| Type de bloc | `set_secret_goal` |

Bloc importé :

```txt
c:IR1 ?= {
    set_secret_goal = {
        country = c:TUR
        secret_goal = defy
    }
}
```

Justification : le hotfix ajoute exactement ce bloc. Il est cohérent avec la situation HOTFIX-3D où IR1 est protectorat ottoman.

## 6. Vérifications effectuées

- `c:IR1` existe dans `common/country_definitions/02_modded_countries.txt`.
- `c:IR1` a un history country dans `common/history/countries/ir1 - mamluk iraq.txt`.
- `c:TUR` existe dans `common/country_definitions/00_countries.txt`.
- `c:TUR` a un history country dans `common/history/countries/tur - ottoman empire.txt`.
- Aucun bloc `c:IR1 ?= { ... }` n'existait déjà dans `common/history/ai/00_secret_goals.txt`.
- `secret_goal = defy` existe déjà localement, notamment pour `USA -> GBR`.
- `defy` est aussi présent dans la vanilla The Great Wave, notamment dans `common/ai_strategies/02_subject_diplomatic_strategies.txt`.

## 7. Ce qui n'a pas été importé

- Aucun autre secret goal du hotfix.
- Aucune diplomatie.
- Aucun diplomatic play.
- Aucun state, pop ou bâtiment.
- Aucune formation militaire.
- Aucun pays.
- Aucune localisation.
- Aucun événement.
- Aucun fichier `map_data`.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Aucun changement aux lois HOTFIX-2.

## 8. Risques restants

- `defy` peut rendre IR1 plus hostile envers l'Empire ottoman, ce qui est voulu par le hotfix mais doit être observé en jeu.
- Le comportement IA réel dépend aussi du poids stratégique, de la puissance relative et du protectorat existant.
- Aucun autre réglage IA du hotfix n'a été importé.

## 9. Tests à faire en jeu

1. Lancer le mod seul.
2. Démarrer une partie en 1776.
3. Vérifier qu'IR1 existe comme protectorat ottoman.
4. Observer le comportement diplomatique d'IR1 envers TUR pendant plusieurs mois.
5. Vérifier que le diplomatic play régional reste visible.
6. Surveiller `error.log`.
7. Rechercher dans les logs : `IR1`, `TUR`, `secret_goal`, `defy`, `00_secret_goals`.

## 10. Liste exacte des fichiers modifiés

- `common/history/ai/00_secret_goals.txt`
- `docs/reports/hotfix/HOTFIX_3F_IR1_SECRET_GOAL.md`

## 11. Confirmation de périmètre

- Aucune diplomatie modifiée.
- Aucun diplomatic play modifié.
- Aucun state, pop ou bâtiment modifié.
- Aucune formation militaire modifiée.
- Aucun changement BIC, Japon, Inde, NAVY ou ADMIN.
- Le stash MARATH n'a pas été appliqué ni modifié.
