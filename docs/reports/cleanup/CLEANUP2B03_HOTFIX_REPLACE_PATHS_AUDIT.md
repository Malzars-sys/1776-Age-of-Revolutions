# CLEANUP-2B-0.3 — Modern Metadata Finalization & Hotfix Replace Paths Audit

Date : 2026-08-11

Branche : `cleanup-post-release`

HEAD : `25e346efd7c9ea247ad5946e8a756c2467c21ea2`

Version cible : Victoria 3 1.13 / The Great Wave

Périmètre : finalisation du metadata moderne, packaging Workshop et audit statique des onze `replace_paths` du hotfix 2.3.0. Aucun personnage, template ou autre `replace_path` actif n'est ajouté pendant cette phase.

## 1. Character isolation runtime result

Le runtime utilisateur du 11 août 2026 à 15:21–15:31 est un PASS. `logs/debug.log` ne contient plus `Expected member (game_custom_data)`, ne charge plus `common/history/characters/chi - china.txt` et ne référence aucun des fichiers vanilla de character history précédemment actifs. Ses deux seules références de character history, `ir1 - mamluk iraq.txt` et `aus.txt`, correspondent à des fichiers du fork.

Le log monte exactement une source utilisateur, le fork attendu, après le jeu et les 17 DLC. Aucune erreur VFS massive nouvelle n'est présente. Le constat visuel utilisateur (Daoguang et Maria II absents, rulers génériques temporaires) confirme l'isolation.

```text
METADATA_PARSE_ERROR_GONE = YES
VANILLA_CHARACTER_HISTORY_EXCLUDED = YES
CLEANUP2B0_RUNTIME_VALIDATED = YES
```

## 2. Metadata final architecture

`.metadata/metadata.json` conserve les champs du fork et contient une seule politique VFS :

```json
"game_custom_data": {
  "multiplayer_synchronized": true,
  "replace_paths": [
    "common/history/characters"
  ]
}
```

Le JSON est valide. La liste active reste volontairement à une entrée. Le `replace_path` singulier legacy a été retiré du `descriptor.mod` interne ; le `.mod` externe local n'a pas été modifié.

## 3. Git tracking

`.gitignore` ignore désormais `.metadata/*`, puis réautorise uniquement `.metadata/metadata.json`. `git status --short --untracked-files=all` affiche bien `?? .metadata/metadata.json`. Le fichier est donc versionnable sans exposer d'autres contenus cachés du dossier. Aucun staging n'a été effectué et l'index reste vide.

## 4. Workshop packaging

Le manifeste de shipping classe maintenant `.metadata/metadata.json` comme runtime requis. Le builder :

- autorise exactement ce fichier sous `.metadata` et continue de refuser les autres contenus cachés/de développement ;
- échoue si le fichier manque ;
- parse son JSON et échoue si `game_custom_data`, `replace_paths` ou `common/history/characters` manque ;
- conserve le comportement existant de `descriptor.mod` et du reste du payload.

Le test réel du builder a copié 859 fichiers (112 726 810 octets), avec 859 hashes identiques, zéro pollution, zéro secret, zéro chemin développeur et le metadata présent/validé dans le package.

## 5. Hotfix replace_paths inventory

Source vanilla auditée : `C:/Games/Victoria 3 The Great Wave/game` (1.13.0 chargée par le runtime). Source hotfix : `1776_Age_of_Revolutions_hotfix_source` 2.3.0. Les comptes sont récursifs et portent sur les fichiers présents directement sous chaque chemin ; aucun des 17 DLC montés ne fournit de fichier supplémentaire sous ces onze chemins dans cette installation.

`CURRENT_VANILLA_INHERITANCE` désigne les fichiers vanilla sans collision exacte de chemin actuellement visibles en mode fusionné. Le chemin characters actif est l'exception : son remplacement validé réduit cet héritage à zéro.

## 6. Per-path fork/vanilla coverage

| PATH | VANILLA_FILES | FORK_FILES | HOTFIX_FILES | CURRENT_VANILLA_INHERITANCE | FORK_COVERAGE | KNOWN_DEPENDENCIES | TOTAL_CONVERSION_INTENT | RISK | RECOMMENDATION |
|---|---:|---:|---:|---|---|---|---|---|---|
| `common/history/characters` | 262 | 13 | 13 | 0 (isolé) | 3 collisions, 10 fichiers propres ; couverture sélective 1776 assumée | Les pays sans ruler fourni reçoivent un générique ; les templates restent dans `common/character_templates` | Oui, démontré en runtime | Moyen : futurs characters vanilla volontairement exclus | `ADD_REPLACE_PATH_NOW` (déjà actif) |
| `common/history/character_templates` | 0 | 0 | 0 | 0 | Chemin absent partout | Le moteur 1.13 charge `common/character_templates` (210 vanilla, 27 fork) | Non démontré ; entrée legacy vide | Faible en effet, élevé en confusion | `OBSOLETE_OR_INVALID_PATH` |
| `common/history/diplomatic_plays` | 5 | 5 | 5 | 2 : Carlist War, Fezzan revolt | 3 collisions modifiées/neutralisées + 2 setups 1776 propres | Les deux fichiers hérités lancent des guerres de setup 1836 ; aucun identifiant requis pour le setup 1776 | Oui, très fort | Faible à moyen | `ADD_REPLACE_PATH_NOW` |
| `common/history/diplomacy` | 6 | 4 | 4 | 2 : embargos, favors | 4/4 fichiers du fork modifient le setup ; omissions vanilla explicites | Les omissions ajoutent l'embargo TUR–MON et des obligations GRE/POR de 1836 ; données de démarrage autonomes | Oui, très fort | Faible à moyen | `ADD_REPLACE_PATH_NOW` |
| `common/history/interests` | 0 | 0 | 1 | 0 | Aucun fichier dans le fork ; un `00_interests.txt` seulement dans la source hotfix | Le fichier source utilise 29 blocs pays et des strategic regions ; Basileia 1.13 emploie aussi ce chemin, mais le fork actif ne livre rien | Plausible, non matérialisé dans le fork | Moyen : path sans payload et sans test runtime | `AUDIT_DEEPER` |
| `common/history/treaties` | 1 | 1 | 1 | 0 (collision exacte) | Remplacement complet : 29 traités, dont des accords 1775 | Dépend des treaty articles/goods/country tags, qui restent fournis hors du chemin | Oui, très fort | Faible à moyen ; nouveaux traités vanilla futurs seraient exclus | `ADD_REPLACE_PATH_NOW` |
| `common/history/military_deployments` | 1 | 1 | 1 | 0 (collision exacte) | Wrapper vide intentionnel, contre 141 lignes de déploiements de guerres 1836 vanilla | Aucun template ou front vanilla conservé par ce fichier vide | Oui, neutralisation complète | Faible | `ADD_REPLACE_PATH_NOW` |
| `common/flag_definitions` | 2 | 3 | 3 | 0 (2 collisions exactes) | Les 2 noms vanilla sont couverts (1 identique, 1 modifié) + `07_NM_Flags.txt` | Très couplé aux CoA, triggers, variables, sujets et contenu pays ; risque surtout futur | Oui probable | Moyen à élevé en cas d'update/DLC | `AUDIT_DEEPER` |
| `common/dynamic_country_names` | 2 | 2 | 2 | 0 (2 collisions exactes ; le `.md` n'est pas runtime) | Fichier runtime principal modifié, documentation identique | Très couplé aux JEs, mouvements, variables, lois et tags | Oui probable | Moyen à élevé en cas d'update/DLC | `AUDIT_DEEPER` |
| `events` | 330 | 315 | 342 | 27 fichiers vanilla | 303 collisions + 12 fichiers propres ; 27 fichiers 1.13 absents du fork | Au moins 16 des 27 fichiers absents ont des références directes depuis on_actions, history ou JEs du fork | Déclaré par le hotfix, mais snapshot courant incomplet | Critique : systèmes vanilla/DLC supprimés ou gelés | `DO_NOT_REPLACE` |
| `common/journal_entries` | 173 | 170 | 182 | 12 fichiers vanilla | 161 collisions + 9 fichiers propres ; 12 fichiers 1.13 absents du fork | Au moins 5 des 12 fichiers absents sont référencés par AI strategies, on_actions, events ou history | Déclaré par le hotfix, mais snapshot courant incomplet | Critique : systèmes et chaînes event/JE cassés | `DO_NOT_REPLACE` |

Collisions exactes fork/vanilla : characters 3, diplomatic plays 3, diplomacy 4, treaties 1, deployments 1, flags 2, dynamic names 2, events 303, journal entries 161. Le hotfix contient tous les 330 events vanilla et tous les 173 JEs vanilla, plus son contenu propre ; il s'agit donc largement d'un snapshot copié, pas d'une preuve qu'un remplacement global est sûr face aux mises à jour.

## 7. Dependency risks

Les dépendances critiques sont concrètes : le fork référence des namespaces de fichiers events qu'il n'embarque pas, notamment depuis `00_code_on_actions.txt`, des JEs et l'historique global/pays. Exemples : `peru_bolivia_events`, `french_pretenders`, `native_resettlement`, `poland_events`, `sick_man`, `tanzimat_events`, `texan_war_of_independence`, `victoria` et `zanzibar`. Remplacer `events` aujourd'hui supprimerait ces définitions tout en laissant leurs appels.

De même, parmi les JEs absentes du fork, `00_oregon.txt`, `05_serbia.txt`, `06_iberia.txt`, `06_the_carlist_wars.txt` et `06_the_two_spains.txt` ont déjà des références externes. Les supprimer par VFS créerait des références orphelines. Les events/JEs du hotfix 2.3.0 couvrent davantage la vanilla 1.13, mais les recopier ou activer leurs replace paths sans resynchronisation et runtime ciblé figerait aussi les contenus de mise à jour/DLC.

`common/flag_definitions` et `common/dynamic_country_names` ont une couverture de basename complète aujourd'hui, mais leurs triggers dépendent d'un large graphe de CoA, variables, lois, mouvements et JEs. Leur isolation n'apporte pas de correction immédiate et augmenterait le risque d'update.

`common/history/character_templates` est distinct du chemin valide `common/character_templates`. Le premier est absent du jeu 1.13, du fork et même du payload hotfix ; le second est chargé par le runtime et fournit encore 210 fichiers vanilla face à 27 fichiers du fork. Il ne doit pas être remplacé.

## 8. Safe candidates

Les candidats statiquement sûrs pour de futurs tests contrôlés sont :

1. `common/history/diplomatic_plays` ;
2. `common/history/diplomacy` ;
3. `common/history/treaties` ;
4. `common/history/military_deployments`.

Ils décrivent exclusivement le setup initial et le fork matérialise une intention 1776 claire. Aucun n'est ajouté pendant CLEANUP-2B-0.3.

`common/history/interests` reste un candidat fonctionnel possible, mais pas encore sûr : le payload nécessaire existe dans le hotfix/Basileia, pas dans le fork actif. Il faut d'abord décider de sa restauration/migration et prouver son chargement 1.13.

## 9. Dangerous candidates

- `events` et `common/journal_entries` : `DO_NOT_REPLACE` dans l'état actuel ; pertes et références orphelines démontrées.
- `common/flag_definitions` et `common/dynamic_country_names` : audit plus profond avant isolation ; aucun bénéfice immédiat par rapport aux collisions actuelles.
- `common/history/character_templates` : entrée obsolète/invalide à supprimer d'un futur metadata, sans jamais la convertir en `common/character_templates`.

## 10. Proposed future VFS batches

- **VFS-1 — initial diplomatic setup** : tester `common/history/diplomatic_plays` puis `common/history/diplomacy`, avec contrôle des guerres American Revolution/Otto-Iraqi-Persia et absence de Carlist/Fezzan + embargos/obligations 1836.
- **VFS-2 — treaties, puis interests** : isoler d'abord `common/history/treaties`. Traiter `common/history/interests` dans un sous-test séparé seulement après ajout volontaire de son payload au fork et preuve de parsing/runtime.
- **VFS-3 — military deployment history** : isoler `common/history/military_deployments` et vérifier qu'aucun front/armée 1836 n'est pré-déployé.
- **VFS-4 — flag/dynamic country infrastructure** : audit des CoA, triggers, variables, localisations et JEs avant tout changement.
- **VFS-5 — events/journal entries** : ne considérer qu'après resynchronisation exhaustive avec la version cible, audit des namespaces/IDs et justification fonctionnelle explicite. Le défaut recommandé reste la fusion.

Chaque batch doit ajouter un nombre minimal de chemins, avoir un diff metadata isolé, un audit statique, un runtime utilisateur ciblé et un rollback consistant à retirer ces seules entrées.

## 11. Protected-state verification

- Les sept fichiers de recherche technologique restent présents, untracked et unstaged ; leurs hashes SHA-256 ont été relevés sans écriture.
- Aucun fichier sous `common/history/characters`, `common/character_templates` ou `common/history/character_templates` n'est modifié ou créé.
- BIC conserve `activate_law = law_type:law_frontier_colonization` et ne contient pas `law_colonial_exploitation`.
- Aucune entrée nommée exactement `bject` n'existe hors internals Git.
- L'index Git est vide ; aucune commande Git mutante n'a été exécutée.
- Codex n'a lancé ni Victoria 3 ni le launcher.

## 12. Final verdict

L'architecture VFS moderne est maintenant validée en runtime, versionnable et packageable. La reconstruction historique des rulers majeurs peut commencer dans une phase distincte, puisque l'héritage des rulers vanilla 1836 est effectivement coupé. Les rulers génériques restent seulement des placeholders jusqu'à cette reconstruction.

```text
CLEANUP2B0_RUNTIME_VALIDATED = YES
METADATA_CHARACTER_REPLACE_PATH_RUNTIME = PASS
METADATA_TRACKABLE_BY_GIT = YES
WORKSHOP_BUILDER_INCLUDES_METADATA = YES

ACTIVE_REPLACE_PATH_COUNT = 1
ACTIVE_REPLACE_PATH_1 = common/history/characters

LEGACY_INTERNAL_REPLACE_PATH_REMOVED = YES
LEGACY_EXTERNAL_DESCRIPTOR_MODIFIED_BY_CODEX = NO

HOTFIX_REPLACE_PATHS_AUDIT_COMPLETE = YES
SAFE_ADDITIONAL_REPLACE_PATHS_IDENTIFIED = YES
EVENTS_REPLACE_PATH_ADDED = NO
JOURNAL_ENTRIES_REPLACE_PATH_ADDED = NO
CHARACTER_TEMPLATES_REPLACE_PATH_ADDED = NO

V13_STATIC_VALIDATION = PASS
CODEX_LAUNCHED_VICTORIA3 = NO
SAFE_TO_BEGIN_HISTORICAL_RULER_RECONSTRUCTION = YES
```

STOP.
