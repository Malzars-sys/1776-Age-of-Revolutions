# LOG-CLEANUP-2 — Alignement du modifier de capacité des convois avec Victoria 3 1.13

Date d'audit : 14 août 2026

Mode : `STATIC / BOUNDED GAMEPLAY PATCH / HUMAN RUNTIME VALIDATED`

Famille : `API_COUNTRY_CONVOYS_CAPACITY_MULT`

## État de la phase

```text
LOG_CLEANUP_2 = PASS
DECISION_BRANCH = EXACT_OR_STRONGLY_EQUIVALENT_SUCCESSOR
SAFE_ATOMIC_REPLACEMENT = YES
GAMEPLAY_CHANGE_APPLIED = YES
RUNTIME_EXECUTED_BY_CODEX = NO
RUNTIME_EXECUTED_BY_HUMAN = YES
```

La preuve statique autorise un remplacement atomique. L'opérateur humain a ensuite ouvert Victoria 3 avec le fork monté et l'a quitté proprement ; Codex n'a pas lancé le jeu. La nouvelle génération ciblée ne reproduit ni l'ancienne erreur ni une erreur attribuable au remplacement.

## Préflight Git

```text
BRANCH = post-2.3.0-log-cleanup
HEAD = 901356ba7f4776ecf880b03065213a9b83096b5a
HEAD_SUBJECT = Document release 2.3.0 log cleanup baseline
WORKTREE_BEFORE = CLEAN
INDEX_BEFORE = EMPTY
LOG_CLEANUP_1_COMMITTED = YES
```

Le préflight a été effectué avant toute écriture. Aucun changement inattendu n'était présent.

## Diagnostic ciblé

LOG-CLEANUP-1 contient exactement une identité et une occurrence de cette famille :

```text
DIAGNOSTIC_TYPE = PARSER
SOURCE_LOG = debug.log
TARGET_DIAGNOSTIC = Unknown modifier type: country_convoys_capacity_mult. It is either invalid, or a potential dynamic modifier type definition missing from the database.: country_convoys_capacity_mult
TARGET_FILE = common/company_types/02_new_companies.txt
TARGET_BASELINE_LINE = 53
TARGET_OBJECT = company_dutch_east_india_company
COUNT = 1
OCCURRENCES = 1
LOG_CLEANUP_1_CLASSIFICATION = FORK_ATTRIBUTABLE_FIXABLE
HOTFIX_6A28_CLASSIFICATION = POST_MERGE_BACKLOG
```

La classification `FIXABLE` était une sélection d'audit, pas encore la preuve d'un successeur. HOTFIX-6A.26 n'avait autorisé aucune transformation mécanique et HOTFIX-6A.28 avait différé le choix après le merge.

## Sémantique historique

```text
OLD_MODIFIER = country_convoys_capacity_mult
OLD_SCOPE = country
OLD_VALUE = 0.2
OLD_VALUE_TYPE = multiplicative percentage
OLD_EFFECT = +20 % à la capacité nationale de convois de l'ancien système
OLD_GAMEPLAY_PURPOSE = accroître la capacité logistique maritime civile disponible grâce à la prospérité de l'East India Company/VOC
```

Le suffixe `_mult` et la valeur positive encodent un multiplicateur en pourcentage. Dans le système antérieur à 1.13, les convois constituaient une capacité nationale employée pour les connexions et échanges maritimes. La refonte 1.13 répartit cette ancienne fonction entre la marine marchande, les voies maritimes et les supply ships ; une similarité de nom seule n'aurait donc pas suffi.

## Provenance Git

L'historique du fichier est borné à trois commits :

```text
78e562f Give the VOC a dedicated company identity
3aeb09e Fix high confidence India region references
b602804 Initial import of 1776 Age of Revolutions fork
```

`git log -S"country_convoys_capacity_mult"` attribue l'introduction de la ligne à `b602804`, l'import initial. `git blame` confirme que la ligne est restée inchangée depuis cet import. `3aeb09e` n'a modifié que les régions indiennes. `78e562f` a donné à la VOC son icône, son café et son bien de prestige dédiés sans modifier le `prosperity_modifier`.

Le bloc importé conserve le commentaire et la structure de l'ancienne East India Company : catégorie aristocratique, plantations de thé, tabac et opium/café, extensions soie et sucre, puis un unique bonus de prospérité maritime.

## Registre et exemples vanilla 1.13.9

Installation auditée : `C:\Games\Victoria 3`, version runtime de référence `release/1.13.9 : afea32b87`, DLC The Great Wave.

La recherche de `country_convoys_capacity_mult` dans toute l'installation vanilla retourne zéro fichier. Les candidats réellement enregistrés ont ensuite été comparés par scope, type numérique et effet.

| candidate_modifier | registered_in_1_13_9 | scope | numeric_semantics | gameplay_effect | vanilla_example | semantic_match | selected |
|---|---|---|---|---|---|---|---|
| `country_ship_group_supply_ships_construction_efficiency_add` | YES | country | additive percentage to construction efficiency | augmente l'efficacité de construction du groupe de navires `supply_ships` | `common/company_types/00_companies_asia.txt`, prospérité de `company_east_india_company`, valeur `0.2` | STRONG — homologue officiel exact de l'objet importé | YES |
| `state_trade_capacity_mult` | YES | state | multiplicative percentage | augmente la capacité commerciale des États | plusieurs prospérités, dont `00_companies_cots.txt` et `00_companies_soi.txt` | NO — ressource et scope différents | NO |
| `country_port_connection_cost_mult` | YES | country | multiplicative percentage, signe favorable négatif | réduit la demande de marine marchande des seules connexions portuaires | `common/power_bloc_principles/00_power_bloc_principles.txt` | NO — coût d'un sous-ensemble de voies, pas capacité maritime | NO |
| `goods_output_merchant_marine_add` | YES | building | flat goods output | ajoute une quantité fixe de marine marchande produite par les bâtiments | `common/production_methods/11_private_infrastructure.txt` | NO — scope bâtiment et valeur absolue | NO |
| `country_supply_ship_construction_ratio_add` | YES | country | additive ratio | règle l'allocation de construction des supply ships | `common/static_modifiers/00_code_static_modifiers.txt` | NO — contrôle d'allocation, pas bonus de prospérité | NO |

La définition sélectionnée se trouve dans `common/modifier_type_definitions/00_modifier_types.txt` et déclare `percent = yes`. Son exemple décisif est l'homologue vanilla 1.13.9 :

```text
# United Company of Merchants of England Trading to the East Indies
company_east_india_company = {
    ...
    prosperity_modifier = {
        country_ship_group_supply_ships_construction_efficiency_add = 0.2
    }
}
```

Cet objet possède le même commentaire historique, la même icône EIC d'origine, la même catégorie aristocratique, les mêmes familles de plantations et la même organisation générale que le bloc dont dérive la VOC du fork. Il constitue une migration vanilla directe, et non une inférence fondée sur le seul nom « supply ships ».

## Décision

```text
VALID_1_13_MODIFIER = YES
COUNTRY_SCOPE_COMPATIBLE = YES
PROSPERITY_MODIFIER_COMPATIBLE = YES
SEMANTIC_PURPOSE_PRESERVED = YES
VALUE_0_2_PRESERVABLE = YES
SELECTED_1_13_MODIFIER = country_ship_group_supply_ships_construction_efficiency_add
SELECTED_VALUE = 0.2
```

Le nouveau suffixe `_add` décrit l'addition au taux d'efficacité de construction, tandis que l'ancien `_mult` décrivait un multiplicateur de capacité. La valeur ne serait pas transférable sur ce seul constat. Elle est néanmoins conservable ici parce que la vanilla 1.13.9 a migré l'homologue exact de la compagnie vers ce modifier avec exactement `0.2`.

## Correctif exact

```diff
 prosperity_modifier = {
-    country_convoys_capacity_mult = 0.2
+    country_ship_group_supply_ships_construction_efficiency_add = 0.2
 }
```

```text
TARGET_FILE_SHA256_BEFORE = 3A739EC2848660C89452929643582DBD3869B19254FD0FD0C3D117642DCF2478
TARGET_FILE_SHA256_AFTER_GAMEPLAY_PATCH = 5D47E345E44E3FF6575B528FD384E52D9644E5E6D34564670241D3F499B9EEC6
TARGET_FILE_SHA256_FINAL_WITH_USER_COMMENT = 9F8B47494E5CB0265915793E36F9C4FF755EDEDE2AFC1AAD23DC89546925A372
GAMEPLAY_CHANGED_FILES = 1
GAMEPLAY_CHANGED_HUNKS = 1
GAMEPLAY_INSERTIONS = 1
GAMEPLAY_DELETIONS = 1
USER_AUTHORED_COMMENT_HUNKS = 1
TARGET_FILE_TOTAL_CHANGED_HUNKS = 2
TARGET_FILE_TOTAL_INSERTIONS = 2
TARGET_FILE_TOTAL_DELETIONS = 2
```

Le hunk gameplay ne contient aucune modification adjacente. `potential`, `possible`, les listes de bâtiments et biens, `ai_will_do` et tous les autres blocs restent inchangés. Après le runtime, l'utilisateur a corrigé séparément le commentaire de ligne 1 de `United Company of Merchants of England Trading to the East Indies` vers `Vereenigde Oostindische Compagnie`. Ce second hunk non-gameplay est conservé et attribué à l'utilisateur ; il n'est pas compté comme un hunk gameplay du correctif.

## Validation statique

```text
GIT_DIFF_CHECK = PASS
STATIC_LEGACY_OCCURRENCES_BEFORE = 1
STATIC_LEGACY_OCCURRENCES_AFTER = 0
STATIC_SELECTED_MODIFIER_OCCURRENCES_IN_FORK_COMMON = 1
UNEXPECTED_LEGACY_OCCURRENCES = 0
INDEX = EMPTY
```

Le seul fichier gameplay modifié est `common/company_types/02_new_companies.txt`. Le présent rapport est le seul nouveau fichier documentaire.

## Validation runtime humaine

L'opérateur humain a lancé Victoria 3, atteint le menu principal puis quitté le jeu. Une nouvelle partie n'était pas nécessaire pour cette validation de parsing. Les segments frais sont `system.log`, `debug.1.log`, `debug.log`, `error.log`, `game.1.log` et `game.log`, pour une session commencée à `20:49:21` et fermée à `20:55:09` le 14 août 2026.

```text
VICTORIA_3_VERSION = release/1.13.9 : afea32b87
THE_GREAT_WAVE_MOUNTED = YES
TARGET_FORK_DECLARED = YES
TARGET_FORK_MOUNTED = YES
TARGET_FORK_PATH = C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork
SYSTEM_LOG_SHA256 = 1F09059140AC294677A6DC3444A10F8170558EEC1EE74320182CB9ADB82CDEDD
DEBUG_1_LOG_SHA256 = BB267AD199E1A5E1395E852D48DCE88FB1116D735F5C272627A66CA6979EE6AD
DEBUG_LOG_SHA256 = 7660F7D7FD5A91CD136BE8088BF43EE053BC4E97C8B8F5CCD3B04A3DBE95D82C
ERROR_LOG_SHA256 = 795DEE3E85E7F4C091D590388C1E9EC45152781199CB148B8F64FFEE18C6729F
```

La recherche ciblée dans tous ces segments frais, y compris les deux segments `game`, retourne zéro correspondance pour l'ancienne clé, le nouveau modifier, `02_new_companies.txt` et `company_dutch_east_india_company`. L'absence du nouveau modifier comme texte de log est normale lorsqu'il est accepté ; surtout, aucun parser diagnostic ne le cite et aucun diagnostic ne vise le fichier cible.

Résultats ciblés :

```text
TARGET_LEGACY_PARSER_DIAGNOSTIC_BEFORE = 1
TARGET_LEGACY_PARSER_DIAGNOSTIC_AFTER = 0
NEW_TARGET_FILE_PARSER_DIAGNOSTICS = 0
NEW_ATTRIBUTABLE_DIAGNOSTIC_FROM_REPLACEMENT = 0
FUNCTIONAL_EFFECT_RUNTIME_OBSERVED = NO
```

L'effet visuel précis de la prospérité n'a pas été observé au menu principal et aucun PASS visuel n'est revendiqué. Les preuves fonctionnelles sont le registre vanilla, l'homologue vanilla exact, la compatibilité de scope et l'absence de diagnostic dans la génération montée.

## Protections et risques résiduels

```text
TECH_TREE_FILES_CHANGED = 0
HISTORY_FILES_CHANGED = 0
MILITARY_FILES_CHANGED = 0
NAVY_FILES_CHANGED = 0
ADMIN_FILES_CHANGED = 0
UNRELATED_GAMEPLAY_FILES_CHANGED = 0
STAGED_FILES = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
```

Le parsing ciblé est validé. Le risque résiduel est limité à l'absence d'observation visuelle du bonus de prospérité ; aucune nouvelle partie ni manipulation destructive n'a été effectuée pour forcer cette observation.

## Résultat final

```text
LOG_CLEANUP_2 = PASS
BRANCH = post-2.3.0-log-cleanup
HEAD = 901356ba7f4776ecf880b03065213a9b83096b5a
TARGET_DIAGNOSTIC = Unknown modifier type: country_convoys_capacity_mult. It is either invalid, or a potential dynamic modifier type definition missing from the database.: country_convoys_capacity_mult
TARGET_FILE = common/company_types/02_new_companies.txt
OLD_MODIFIER = country_convoys_capacity_mult
OLD_VALUE = 0.2
OLD_SEMANTICS = country-scoped multiplicative percentage; +20 % old national convoy capacity
SELECTED_1_13_MODIFIER = country_ship_group_supply_ships_construction_efficiency_add
SELECTED_VALUE = 0.2
NEW_SEMANTICS = country-scoped additive percentage; +20 % supply-ships construction efficiency, matching the exact vanilla 1.13.9 East India Company homolog
SAFE_ATOMIC_REPLACEMENT = YES
GAMEPLAY_CHANGE_APPLIED = YES
STATIC_LEGACY_OCCURRENCES_BEFORE = 1
STATIC_LEGACY_OCCURRENCES_AFTER = 0
TARGET_LEGACY_PARSER_DIAGNOSTIC_BEFORE = 1
TARGET_LEGACY_PARSER_DIAGNOSTIC_AFTER = 0
NEW_ATTRIBUTABLE_DIAGNOSTICS = 0
FUNCTIONAL_EFFECT_RUNTIME_OBSERVED = NO
GAMEPLAY_CHANGED_FILES = 1
GAMEPLAY_CHANGED_HUNKS = 1
GAMEPLAY_FILES_CHANGED = common/company_types/02_new_companies.txt
DOCUMENTATION_FILES_CREATED = docs/reports/log_cleanup/LOG_CLEANUP_2_CONVOYS_CAPACITY_MODIFIER.md
TECH_TREE_FILES_CHANGED = 0
STAGED_FILES = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
```

Le fichier gameplay possède aussi un second hunk de commentaire, explicitement écrit par l'utilisateur après le runtime. Il ne modifie aucune sémantique gameplay et n'est pas compté dans `GAMEPLAY_CHANGED_HUNKS`.

## Suite proposée

```text
NEXT_PHASE = LOG-CLEANUP-3-HAS-TECHNOLOGY-RESEARCHED
```

Cette famille ne contient qu'une identité dans LOG-CLEANUP-1. Elle devra être réauditée séparément ; elle n'est pas commencée ici.
