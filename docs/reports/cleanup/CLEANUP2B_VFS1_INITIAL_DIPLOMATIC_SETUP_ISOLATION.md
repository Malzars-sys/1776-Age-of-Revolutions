# CLEANUP-2B-VFS-1 — Initial Diplomatic Setup Isolation

Date : 2026-08-11

Branche : `cleanup-post-release`

HEAD de baseline : `1e669d7f55e1ba89ed997f0b4495cc871600de4d`

Version cible : Victoria 3 1.13 / The Great Wave

## 1. Baseline

La baseline a été vérifiée avant toute édition : branche et HEAD conformes, `git diff --check` sans erreur et index vide. Les seuls fichiers non suivis étaient le rapport naval antérieur et les sept recherches technologiques protégées.

Le metadata était un JSON valide contenant exactement :

```json
"replace_paths": [
  "common/history/characters"
]
```

Le rapport `CLEANUP2B03_HOTFIX_REPLACE_PATHS_AUDIT.md` a été lu intégralement. Aucun ruler ou fichier de personnage n'entre dans le périmètre de VFS-1.

## 2. Diplomatic plays inheritance

Inventaire vanilla exact :

1. `00_carlist_war.txt` — vanilla only ;
2. `00_fezzan_revolt.txt` — vanilla only ;
3. `00_ladakh_war.txt` — collision exacte de chemin ;
4. `00_south_american_wars.txt` — collision exacte de chemin ;
5. `00_texan_war_of_independence.txt` — collision exacte de chemin.

Inventaire fork exact :

1. `00_american_revolution.txt` — fork only ;
2. `00_ladakh_war.txt` — collision, remplacé par un dummy ;
3. `00_otto_iraqi_persia_war.txt` — fork only ;
4. `00_south_american_wars.txt` — collision, remplacé par un dummy ;
5. `00_texan_war_of_independence.txt` — collision, remplacé par un dummy.

Avant VFS-1, les cinq fichiers du fork et les deux fichiers vanilla sans collision formaient un ensemble effectif de sept fichiers.

| FILE | VANILLA_ONLY_OR_COLLISION | CONTENT | START_DATE_OR_CONTEXT | COUNTRIES | VALID_FOR_1776 | ACTION |
|---|---|---|---|---|---|---|
| `00_carlist_war.txt` | Vanilla only | Crée immédiatement une révolution nommée `first_carlist_war`, en guerre civile, visant la capitale espagnole ; résout aussi le play pour CUB, PHI et PCO | Setup du bookmark vanilla 1836 ; la Première guerre carliste commence après la mort de Ferdinand VII en 1833 | SPC, SPA, CUB, PHI, PCO | NO | Exclure par `replace_paths` |
| `00_fezzan_revolt.txt` | Vanilla only | TRI lance immédiatement une guerre d'annexion sur la capitale de FZN ; FZN reçoit un war goal de révocation des claims de TRI | Setup inconditionnel du bookmark 1836, sans date interne ; révolte/politique tripolitaine de ce contexte | TRI, FZN | NO | Exclure par `replace_paths` |
| `00_ladakh_war.txt` | Collision | Vanilla : guerre KAS–LAD active ; fork : fichier dummy | Guerre commencée en 1834 et active dans le setup 1836 | KAS, LAD | NO | Conserver le dummy du fork |
| `00_south_american_wars.txt` | Collision | Vanilla : Ragamuffin War et Cabanagem ; fork : fichier dummy | Soulèvements de 1835 intégrés au setup 1836 | BRZ, PNI, PRA | NO | Conserver le dummy du fork |
| `00_texan_war_of_independence.txt` | Collision | Vanilla : guerre d'indépendance Texas–Mexique ; fork : fichier dummy | Guerre 1835–1836 | TEX, MEX | NO | Conserver le dummy du fork |
| `00_american_revolution.txt` | Fork only | Guerre d'indépendance USA–GBR avec backers coloniaux, FRA et SPA, et war goals 1776 propres au fork | Révolution américaine au 1er janvier 1776 | USA, GBR, SC1–SC4, SPA, FRA | YES | Conserver |
| `00_otto_iraqi_persia_war.txt` | Fork only | Play PER–IR1, backer OMA et war goals sur Basra, Khuzestan et Fars | Setup géopolitique 1776 du fork | PER, IR1, OMA, ARB | YES | Conserver |

Conclusion : Carlist War et Fezzan revolt sont bien les deux contaminations vanilla 1836 encore héritées. Le remplacement de répertoire ramène l'ensemble effectif aux cinq fichiers explicitement livrés par le fork.

## 3. Diplomacy inheritance

Inventaire vanilla exact : `00_embargos.txt`, `00_favors.txt`, `00_relations.txt`, `00_rivalries.txt`, `00_subject_relationships.txt`, `00_truces.txt`.

Inventaire fork exact : `00_relations.txt`, `00_rivalries.txt`, `00_subject_relationships.txt`, `00_truces.txt`.

Les quatre noms du fork sont des collisions et constituent son setup explicite : 232 relations, 10 pactes de rivalité, 92 pactes de sujet et un fichier de trêves vide. Les deux fichiers vanilla sans collision étaient donc encore hérités.

| FILE | EFFECT | COUNTRIES | 1836_SETUP | VALID_FOR_1776 | ACTION |
|---|---|---|---|---|---|
| `00_embargos.txt` | Crée un pacte diplomatique de type `embargo` de TUR vers MON | TUR, MON | YES | NO : relation injectée uniquement par le setup vanilla, sans justification dans le setup 1776 du fork | Exclure par `replace_paths` |
| `00_favors.txt` | Crée quatre obligations : GRE doit une obligation à RUS, FRA et GBR ; POR doit une obligation à SPA | GRE, RUS, FRA, GBR, POR, SPA | YES | NO : obligations propres à la situation diplomatique du bookmark 1836 | Exclure par `replace_paths` |

Les relations, rivalités et relations de sujet voulues par le fork restent intactes. Aucun autre type de relation ne disparaît avec les deux fichiers vanilla-only.

## 4. Dependency audit

### Diplomatic plays

- Les deux fichiers vanilla ne définissent aucun type de diplomatic play, war goal, pays, journal entry ou scripted effect ; ils instancient seulement des objets de démarrage à partir de types définis ailleurs.
- `first_carlist_war` est le seul nom d'instance créé. Aucune référence exacte à ce nom n'existe dans le fork hors du fichier vanilla absent.
- Le fork conserve des systèmes carlistes génériques et tardifs, mais son `common/history/global/00_global.txt` commente l'ajout initial de `je_the_first_carlist_war`, et `carlist_war.7` n'a aucun appel de démarrage dans le fork. Ils ne dépendent donc pas de l'instance 1836 supprimée.
- Le fichier Fezzan ne crée aucun nom ni saved scope. Les usages de FZN/TRI ailleurs ne dépendent pas de cette guerre initiale.
- Les trois guerres vanilla déjà neutralisées le sont par des dummies explicites ; le remplacement de répertoire ne change pas cet état.

### Diplomacy

- `00_embargos.txt` ne crée aucun identifiant : il ajoute seulement un pacte initial TUR–MON.
- `00_favors.txt` ne crée ni ID ni saved scope : il applique quatre états d'obligation initiaux.
- Les événements, on_actions et AI strategies qui utilisent génériquement les mécaniques d'embargo et d'obligation conservent leurs types et effets. Ils ne sont pas définis dans les fichiers supprimés.
- Les stratégies TUR–MON présentes dans le fork sont conditionnées par les JEs de raids monténégrins, pas par l'embargo initial.
- L'événement colonial portugais qui teste une obligation envers GBR peut créer cette obligation lui-même ; il ne dépend pas de l'obligation vanilla POR→SPA supprimée. Les tests d'obligation envers RUS trouvés concernent la Chine et non GRE.

```text
KNOWN_BREAKING_DEPENDENCIES_DIPLOMATIC_PLAYS = NONE
KNOWN_BREAKING_DEPENDENCIES_DIPLOMACY = NONE
DEPENDENCY_AUDIT_CONFIDENCE = HIGH

DIPLOMATIC_PLAYS_REPLACE_SAFE = YES
DIPLOMACY_REPLACE_SAFE = YES
CARLIST_WAR_1836_INHERITANCE_CONFIRMED = YES
FEZZAN_REVOLT_1836_INHERITANCE_CONFIRMED = YES
VANILLA_1836_DIPLOMACY_CONTAMINATION_CONFIRMED = YES
```

## 5. Metadata change

Seule la liste `game_custom_data.replace_paths` a changé. Son état final est exactement :

```json
"replace_paths": [
  "common/history/characters",
  "common/history/diplomatic_plays",
  "common/history/diplomacy"
]
```

Aucun autre champ metadata et aucun autre `replace_path` n'a été modifié ou ajouté.

## 6. Before / after VFS

Le calcul avant remplacement est `fork + vanilla - collisions exactes`. Après remplacement, seuls les fichiers du fork sont visibles dans chacun des deux répertoires.

```text
DIPLOMATIC_PLAYS_EFFECTIVE_FILES_BEFORE = 7
DIPLOMATIC_PLAYS_EFFECTIVE_FILES_AFTER = 5

DIPLOMACY_EFFECTIVE_FILES_BEFORE = 6
DIPLOMACY_EFFECTIVE_FILES_AFTER = 4

VANILLA_1836_DIPLOMATIC_PLAY_FILES_AFTER = 0
VANILLA_1836_DIPLOMACY_FILES_AFTER = 0
```

Fichiers éliminés statiquement de la vue VFS :

- `common/history/diplomatic_plays/00_carlist_war.txt` ;
- `common/history/diplomatic_plays/00_fezzan_revolt.txt` ;
- `common/history/diplomacy/00_embargos.txt` ;
- `common/history/diplomacy/00_favors.txt`.

## 7. Workshop package validation

Le builder conserve son architecture et valide maintenant explicitement les trois chemins actifs dans le metadata packagé. Une absence de `common/history/diplomatic_plays` ou `common/history/diplomacy` provoque une erreur dédiée, comme c'était déjà le cas pour characters.

La reconstruction statique autorisée a réussi :

```text
FILES_COPIED = 859
FILES_HASH_MATCH = 859
FILES_HASH_MISMATCH = 0
DEVELOPMENT_POLLUTION_FOUND = 0
POTENTIAL_SECRET_HITS = 0
LOCAL_DEVELOPER_PATH_LEAKS = 0
WORKSHOP_METADATA_CHARACTER_REPLACE_PATH_PRESENT = yes
WORKSHOP_METADATA_DIPLOMATIC_PLAYS_REPLACE_PATH_PRESENT = yes
WORKSHOP_METADATA_DIPLOMACY_REPLACE_PATH_PRESENT = yes
```

Aucune publication Steam n'a été effectuée.

## 8. USER runtime plan

Effectuer une seule session ciblée :

1. fermer complètement Victoria 3, puis lancer uniquement le fork ;
2. commencer un nouveau scénario au 1er janvier 1776 ;
3. vérifier en Espagne qu'aucune Carlist War de setup 1836 n'est active ;
4. vérifier Tripoli, Fezzan et le voisinage ottoman : aucune Fezzan revolt de setup 1836 ;
5. vérifier TUR/MON : aucun embargo provenant du setup vanilla ;
6. vérifier GRE et POR : aucune des quatre obligations vanilla 1836 ;
7. confirmer que l'American Revolution et le play PER–IR1 propres au fork sont présents ;
8. laisser passer quelques jours, quitter normalement, puis contrôler les logs ;
9. vérifier l'absence de parsing des quatre fichiers vanilla exclus et de toute erreur diplomatique attribuable.

Les rulers génériques sont hors scope et ne doivent pas faire échouer ce test.

Critères du futur PASS runtime :

```text
CARLIST_1836_ABSENT = YES
FEZZAN_1836_ABSENT = YES
VANILLA_1836_DIPLOMACY_ABSENT = YES
FORK_1776_DIPLOMACY_PRESENT = YES
ATTRIBUTABLE_DIPLOMACY_ERRORS = 0
```

## 9. Protected-state verification

- Aucun fichier sous `common/history/characters` n'a été modifié ou créé.
- Les sept recherches technologiques restent untracked, unstaged et inchangées.
- BIC conserve `activate_law = law_type:law_frontier_colonization` et ne contient pas `law_colonial_exploitation`.
- Aucune entrée nommée exactement `bject` n'existe hors internals Git.
- Aucun ruler ou autre personnage n'a été créé.
- L'index Git reste vide et aucune commande Git mutante n'a été exécutée.
- Codex n'a lancé ni Victoria 3 ni le launcher.
- VFS-2 n'a pas été commencé.

## 10. Pending verdict

La validation statique et le package Workshop sont PASS. Le verdict runtime reste en attente de l'unique session utilisateur décrite ci-dessus.

```text
DIPLOMATIC_PLAYS_REPLACE_SAFE = YES
DIPLOMACY_REPLACE_SAFE = YES

ACTIVE_REPLACE_PATH_COUNT = 3
ACTIVE_REPLACE_PATH_1 = common/history/characters
ACTIVE_REPLACE_PATH_2 = common/history/diplomatic_plays
ACTIVE_REPLACE_PATH_3 = common/history/diplomacy

CARLIST_WAR_1836_INHERITANCE_REMOVED_STATIC = YES
FEZZAN_1836_INHERITANCE_REMOVED_STATIC = YES
VANILLA_1836_DIPLOMACY_REMOVED_STATIC = YES

WORKSHOP_METADATA_VALIDATION = PASS

CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES
SAFE_FOR_USER_RUNTIME = YES
```

STOP.
