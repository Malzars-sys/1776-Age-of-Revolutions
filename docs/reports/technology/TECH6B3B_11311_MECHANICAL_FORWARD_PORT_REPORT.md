# TECH6B3B — 1.13.11 Mechanical Forward Port

> Addendum TECH6B3E : les shadows 1.13.11 portés mécaniquement ont depuis reçu des décisions humaines autoritatives. En particulier, Terakoya est sans gate et l'assurance maladie publique dépend de `organized_immunization_campaigns`, pas de `institutionalized_scientific_exchange` ni d'`active_principle_pharmacy`. Les autres gates courants sont récapitulés dans le rapport TECH6B3E; cet addendum ne modifie pas le bilan mécanique historique TECH6B3B.

## Résultat

`TECH6B3B_11311_MECHANICAL_FORWARD_PORT = PASS`

La mini-migration mécanique demandée a été appliquée sur la base vanilla canonique 1.13.11. Le périmètre gameplay introduit par TECH6B3B est limité aux 26 chemins autorisés : 18 chemins de lois (neuf suppressions et neuf créations), sept chemins d'événements (cinq suppressions, une création et une mise à jour consolidée) et un fichier de méthodes de production. Aucun commit ni push n'a été effectué.

## A. État initial

- Dépôt : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`
- Branche source constatée : `tech6b2-society-gameplay-implementation`
- Vanilla canonique : `C:\Games\Victoria 3\game`, version `1.13.11`
- Baseline non committée TECH6B2 préservée : 50 fichiers gameplay, soit 16 fichiers suivis modifiés et 34 fichiers gameplay non suivis.
- Aucun reset, clean, restore global, checkout destructif, stash ou remplacement massif n'a été utilisé.
- Les quatre artefacts TECH6B3A ont été lus avant implémentation et leurs empreintes sont restées inchangées.

Empreintes SHA-256 TECH6B3A avant/après :

| Artefact | SHA-256 |
|---|---|
| `TECH6B3A_11311_UPSTREAM_TREE_RECONCILIATION_REPORT.md` | `04f0d09bce56381f9f6c5b49c918ee4f4dd55eafcd6fd7d69b00cddc05d2723a` |
| `TECH6B3A_11311_VANILLA_DELTA_MATRIX.csv` | `96a9984de0e1b711e61bf252006dbbacb3bf9008c609362fdcfcd369d71162a8` |
| `TECH6B3A_STEAM_MAIN_MOD_DELTA_MATRIX.csv` | `d83ffb54e9e42b4654411d6288943872eacbb92f9fbe4b217c19ebcc70445255` |
| `TECH6B3A_TREE_CORRECTION_REQUIREMENTS_MATRIX.csv` | `ab687ee4c70805922857d98da391fd7747f204b460e34e3c8198399c99e39714` |

## B. Branche

La branche `tech6b3b-11311-mechanical-forward-port` a été créée directement depuis l'état de travail courant, sans commit et sans stash. Les modifications non committées TECH6B2 ont suivi sur la nouvelle branche.

## C. Fichiers modifiés par TECH6B3B

### Lois — 18 chemins

Suppressions :

- `common/laws/00_economic_system.txt`
- `common/laws/00_education_system.txt`
- `common/laws/00_free_speech.txt`
- `common/laws/00_health_system.txt`
- `common/laws/00_land_reform.txt`
- `common/laws/00_policing.txt`
- `common/laws/00_taxation.txt`
- `common/laws/00_trade_policy.txt`
- `common/laws/00_welfare.txt`

Créations sur base vanilla 1.13.11 :

- `common/laws/01_economic_system.txt`
- `common/laws/01_education_system.txt`
- `common/laws/02_free_speech.txt`
- `common/laws/01_health_system.txt`
- `common/laws/01_land_reform.txt`
- `common/laws/01_policing.txt`
- `common/laws/01_taxation.txt`
- `common/laws/01_trade_policy.txt`
- `common/laws/02_welfare.txt`

### Événements — 7 chemins

- création : `events/tech_events/military_tech_events.txt`
- suppression : `events/tech_events/flamethrowers_event.txt`
- suppression : `events/tech_events/military_tech_events_01.txt`
- mise à jour consolidée : `events/tech_events/society_tech_events.txt`
- suppression : `events/tech_events/society_events_01.txt`
- suppression : `events/tech_events/society_events_03.txt`
- suppression : `events/tech_events/society_techs_02.txt`

### Production — 1 chemin

- `common/production_methods/04_plantations.txt`

### Documentation — 1 chemin non-gameplay

- `docs/reports/technology/TECH6B3B_11311_MECHANICAL_FORWARD_PORT_REPORT.md`

Total TECH6B3B : 26 chemins gameplay et ce rapport.

## D–E. Migration détaillée des neuf familles de lois

Chaque nouveau shadow part du fichier vanilla 1.13.11 sous son nouveau chemin. Seuls les deltas TECH6B2 prouvés ont ensuite été réappliqués. Une reconstruction automatique de chaque résultat à partir de vanilla plus ces remplacements autorisés produit un contenu identique au fichier final.

| Ancien chemin supprimé | Nouveau chemin | IDs | Deltas TECH6B2 réappliqués |
|---|---|---:|---|
| `common/laws/00_economic_system.txt` | `common/laws/01_economic_system.txt` | 8 | `law_interventionism` : référence IA `human_rights` → `classical_political_economy`; `law_agrarianism` : référence IA `human_rights` → `political_economy`; `law_laissez_faire` : déverrouillage `international_trade` → `commercial_insurance_markets`. |
| `common/laws/00_education_system.txt` | `common/laws/01_education_system.txt` | 5 | `law_religious_schools`, `law_private_schools` et `law_public_schools` → `organized_elementary_schooling`; `law_terakoya` → `institutionalized_scientific_exchange`. |
| `common/laws/00_free_speech.txt` | `common/laws/02_free_speech.txt` | 4 | `law_censorship` → `periodical_print_networks`. |
| `common/laws/00_health_system.txt` | `common/laws/01_health_system.txt` | 4 | `law_private_health_insurance` et `law_public_health_insurance` → `active_principle_pharmacy`. |
| `common/laws/00_land_reform.txt` | `common/laws/01_land_reform.txt` | 9 | `law_tenant_farmers` : référence IA → `systematic_legal_codification`. |
| `common/laws/00_policing.txt` | `common/laws/01_policing.txt` | 4 | `law_local_police_force` et `law_dedicated_police_force` → `professional_civil_policing`. |
| `common/laws/00_taxation.txt` | `common/laws/01_taxation.txt` | 5 | `law_per_capita_based_taxation` : déverrouillage principal et référence IA → `scientific_metrology`. |
| `common/laws/00_trade_policy.txt` | `common/laws/01_trade_policy.txt` | 6 | `law_mercantilism` et `law_free_trade` → `commercial_insurance_markets`. |
| `common/laws/00_welfare.txt` | `common/laws/02_welfare.txt` | 5 | `law_poor_laws` → `constitutional_government`. |

Résultats :

- `LAW_SHADOW_FAMILIES_MIGRATED = 9`
- `LAW_IDS_AT_DUPLICATION_RISK_BEFORE = 50`
- `LAW_OLD_SHADOW_PATHS_REMAINING = 0`
- `LAW_NEW_SHADOW_PATHS_PRESENT = 9`
- les 50 IDs attendus sont présents une fois dans leur nouveau shadow ;
- `LAW_DUPLICATE_IDS_AFTER = 0` pour ces 50 IDs ;
- `common/laws/00_church_and_state.txt` a conservé son chemin et n'a pas été modifié par TECH6B3B.

## F. Consolidation des événements militaires

Les deux fragments du fork couvraient exactement les cinq objets du fichier vanilla consolidé : `flamethrowers_event.1` et `military_tech_events.401` à `.404`. Aucun objet propre au fork n'a été découvert dans les fragments.

Le fichier `events/tech_events/military_tech_events.txt` est désormais le fichier consolidé et son contenu normalisé est identique au vanilla 1.13.11. Les deux anciens fragments ont été supprimés. Tous les IDs militaires ciblés n'ont plus qu'une définition active.

`military_tech_events.403`, intitulé *A Doctrine of Iron and Steam*, a été conservé exactement comme dans la base vanilla 1.13.11 ; aucun faux delta ne lui a été appliqué.

## G. Deux ports de scopes optionnels

Deux objets d'événements ont reçu le port 1.13.11 demandé :

- `military_tech_events.402` : les quatre accès à `this.commander_military_formation` dans ses filtres de généraux utilisent `?=` ;
- `flamethrowers_event.1` : les deux accès à `this.commander_military_formation` utilisent `?=`.

Il s'agit de `MILITARY_OPTIONAL_SCOPE_PORTS = 2` objets, soit six occurrences syntaxiques prouvées. Aucune occurrence correspondante non optionnelle ne subsiste dans ces deux objets.

## H–I. Consolidation Society

Le fichier `events/tech_events/society_tech_events.txt` a été reconstruit depuis la base vanilla consolidée 1.13.11. L'inspection des anciens fragments a montré qu'ils couvraient exactement les huit objets présents dans cette base et ne contenaient aucun événement propre au fork à préserver. La seule différence textuelle observée dans l'ancien `.104` était un commentaire (`Evelators` au lieu de `Elevators`), sans intention gameplay ; elle n'a pas été transportée.

Les trois fragments redondants ont été supprimés. Le fichier final normalisé est identique au vanilla 1.13.11.

- `SOCIETY_104_PRESENT = YES`, une définition active ;
- `SOCIETY_105_PRESENT = YES`, une définition active ;
- `SOCIETY_EVENT_DUPLICATES_AFTER = 0`.

## J. Banana Plantations

Le patch TECH6B3B dans `common/production_methods/04_plantations.txt` contient exactement deux changements de valeurs :

- `default_building_banana_plantation` : `goods_output_fruit_add = 30` ;
- `automatic_irrigation_building_banana_plantation` : `goods_output_fruit_add = 40`.

Le reste des modifications préexistantes du fichier a été préservé. La technologie `mechanized_irrigation`, les autres PM, les épices et les autres valeurs de balance n'ont pas été modifiés par TECH6B3B.

## K. Sept shadows non reconstructibles

Les sept fichiers hors scope ont été fingerprintés avant intervention puis après implémentation. Leurs empreintes sont identiques :

| Fichier | SHA-256 avant/après |
|---|---|
| `common/ai_strategies/00_default_strategy.txt` | `68490ab1a73abe92a0f54d8d897cf213ecc16a37885cf24f79d7ef21ebe99232` |
| `common/defines/00_defines.txt` | `7006ebb82c97b750ea90d435e616bebfeaed0d68f8e725333e653cdec7486978` |
| `common/journal_entries/02_coffee_and_milk.txt` | `34d42b485ebb311b8eb9902c8346f69c837448a7790d9206c620d63348687a2b` |
| `common/on_actions/00_code_on_actions.txt` | `cc80502933383db73f8fb162d78d605eef8786a338c5c35e4dc8c89ce6a30c81` |
| `events/agitators_events/algeria_events.txt` | `4d73d58f16b01038695453ee7a97c4ca59a0475392f070e964741346395e3388` |
| `gui/building_details_panel.gui` | `60ad21cbeebcfc536de64c5d6535a8d32e8c51c675bf22d0e0b5c6d7a73076a6` |
| `gui/production_methods.gui` | `7a0094ab3cda6b31d82fd60886161fe06b3c54b46c26bf252c970e4814e08c2d` |

`UNRELATED_11311_SHADOW_CHANGES = 0`.

## L. Candidats de correction d'arbre

Aucune des 53 entrées `TREE_CORRECTION_IMPLEMENTATION_CANDIDATES` n'a été implémentée. L'agrégat des six fichiers du namespace technologique contrôlé est resté à `919fbc618c84e3b3b6f3fa4f1e88e6d29b65cbf9202289222ff065c22a6a2a25` avant/après.

`TREE_CORRECTION_CHANGES = 0` et `REPLACE_PATH_TECH_TREE_CHANGES = 0`.

## M. Décisions humaines

Aucune des 24 entrées `TREE_CORRECTION_HUMAN_REVIEW` n'a été tranchée ou préemptée.

`TREE_HUMAN_DECISIONS_PREEMPTED = 0`.

## N. Steam et snapshot 2.3.0.1

Aucun fichier n'a été copié depuis le Workshop et aucun port Steam n'a été réalisé. Le snapshot immutable `1776_Age_of_Revolutions_hotfix_source` compte toujours 842 fichiers. Son empreinte agrégée récursive déterministe est restée identique avant/après :

`46fd3acfcd7f1fb8377963f8f38aa54d9b118556d0bccb353565ecf1e0146a2c`

- `STEAM_FORWARD_PORT_CHANGES = 0`
- `STEAM_2301_BASELINE_CHANGED = NO`

## O. Contrôles statiques

Résultat global : `STATIC_VALIDATION = PASS` avec zéro erreur.

Contrôles exécutés :

- reconstruction des neuf nouveaux shadows depuis vanilla 1.13.11 plus la liste fermée des deltas TECH6B2 ;
- présence, chemin attendu et unicité des 50 IDs de lois ;
- disparition des neuf anciens shadows ;
- comparaison normalisée des deux fichiers d'événements consolidés avec vanilla 1.13.11 ;
- unicité globale de `flamethrowers_event.1`, `military_tech_events.402`, `.403`, `society_tech_events.104` et `.105` ;
- présence des six occurrences `?=` dans les deux seuls objets portés et absence des formes non optionnelles correspondantes ;
- disparition des cinq fragments obsolètes ;
- extraction objet-scopée des deux valeurs Banana, égales à 30 et 40 ;
- contrôle des accolades et guillemets des 26 chemins gameplay de la phase ;
- contrôle des empreintes des sept shadows protégés, des namespaces technologiques, des Starting Technologies, des artefacts TECH6B3A et du snapshot Steam ;
- `git diff --check`, sans erreur (seulement les avertissements de conversion LF/CRLF déjà liés à la configuration Git sous Windows).

L'agrégat des six fichiers Starting Technologies est resté identique : `0c71f92d0645786f2a027c0b34e0870e8a0fd283395d2a7f25c3ebd34175003f`.

Résultats de non-scope :

```text
TREE_CORRECTION_CHANGES = 0
TREE_HUMAN_DECISIONS_PREEMPTED = 0
STEAM_FORWARD_PORT_CHANGES = 0
STARTING_TECH_CHANGES = 0
REPLACE_PATH_TECH_TREE_CHANGES = 0
UNRELATED_11311_SHADOW_CHANGES = 0
NEW_TECH_IDS = 0
NEW_LAW_IDS = 0
NEW_EVENT_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
```

## P. Runtime

`RUNTIME = NOT_CLAIMED`.

Un smoke de chargement parser/log a néanmoins été effectué avec la procédure déjà documentée, via `victoria3.exe -debug_mode -mod=".../descriptor.mod"`. Le journal frais confirme le montage de `1776_Age_of_Revolutions_fork` et le chargement jusqu'aux étapes localisation/interface, sans erreur ciblant les nouveaux shadows de lois, les événements consolidés, les valeurs Banana, un doublon d'objet, une technologie inconnue ou une erreur de parsing imputable au patch.

Le processus a ensuite été arrêté proprement côté test (fermeture de fenêtre indisponible, arrêt forcé du processus de smoke). Les diagnostics de localisation observés sont préexistants et hors scope. Le menu, le setup 1776, le démarrage d'une partie et le passage d'un mois n'ont pas été automatisés ni observés ; aucun `PASS` runtime complet n'est donc revendiqué.

`PARSER_LOG_SMOKE = PASS`.

## Q. Git diff final

Le contrôle `git diff --name-status`, `git diff --stat` et `git diff` a été effectué intégralement. L'état de travail contient simultanément la baseline TECH6B2 préexistante et TECH6B3B ; les nouvelles lignes TECH6B3B sont toutes attribuables à l'une des quatre familles autorisées.

Statistique Git des fichiers **suivis** de l'état de travail après implémentation et avant ajout de ce rapport :

```text
23 files changed, 569 insertions(+), 1059 deletions(-)
```

Cette statistique globale comprend les modifications TECH6B2 antérieures. Elle n'inclut pas les fichiers non suivis, notamment les neuf nouveaux shadows de lois et le nouveau fichier militaire consolidé. L'attribution TECH6B3B fiable est donc la liste fermée de la section C : 26 chemins gameplay. Le rapport est un chemin documentaire supplémentaire.

Aucun commit et aucun push n'ont été effectués.

## R. Anomalies restantes

- Aucune anomalie statique de périmètre ou de contenu n'a été trouvée dans TECH6B3B.
- Les avertissements de localisation du smoke sont préexistants et hors scope.
- La validation runtime complète reste volontairement `NOT_CLAIMED` faute d'observation automatisée du menu, du setup, d'une nouvelle partie et d'un mois de jeu.
- Les sept shadows non reconstructibles, les 53 candidats de correction d'arbre et les 24 décisions humaines restent explicitement différés.

## Sortie terminale

```text
TECH6B3B_11311_MECHANICAL_FORWARD_PORT = PASS

BRANCH = tech6b3b-11311-mechanical-forward-port

VANILLA_CANONICAL_VERSION = 1.13.11

LAW_SHADOW_FAMILIES_TARGETED = 9
LAW_SHADOW_FAMILIES_MIGRATED = 9
LAW_IDS_AT_DUPLICATION_RISK_BEFORE = 50
LAW_OLD_SHADOW_PATHS_REMAINING = 0
LAW_NEW_SHADOW_PATHS_PRESENT = 9
LAW_DUPLICATE_IDS_AFTER = 0

MILITARY_EVENT_CONSOLIDATION = PASS
MILITARY_OPTIONAL_SCOPE_PORTS = 2
MILITARY_EVENT_DUPLICATES_AFTER = 0

SOCIETY_EVENT_CONSOLIDATION = PASS
SOCIETY_104_PRESENT = YES
SOCIETY_105_PRESENT = YES
SOCIETY_EVENT_DUPLICATES_AFTER = 0

BANANA_DEFAULT_FRUIT = 30
BANANA_AUTOMATIC_IRRIGATION_FRUIT = 40
BANANA_PORT = PASS

TREE_CORRECTION_CHANGES = 0
TREE_HUMAN_DECISIONS_PREEMPTED = 0
STEAM_FORWARD_PORT_CHANGES = 0
STARTING_TECH_CHANGES = 0
REPLACE_PATH_TECH_TREE_CHANGES = 0
UNRELATED_11311_SHADOW_CHANGES = 0

STEAM_2301_BASELINE_CHANGED = NO

NEW_TECH_IDS = 0
NEW_LAW_IDS = 0
NEW_EVENT_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0

GAMEPLAY_FILES_CHANGED_BY_TECH6B3B = 26

STATIC_VALIDATION = PASS
RUNTIME = NOT_CLAIMED

COMMIT = NO
PUSH = NO

REPORT =
docs/reports/technology/TECH6B3B_11311_MECHANICAL_FORWARD_PORT_REPORT.md

NEXT_PHASE_READY = YES
```
