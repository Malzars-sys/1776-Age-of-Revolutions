# LOG-CLEANUP-3 — Lot corrigeable à faible risque

Date d'audit : 14 août 2026

Mode : `STATIC / BOUNDED BATCH PATCH / ONE HUMAN RUNTIME VALIDATED`

Version cible : Victoria 3 `release/1.13.9 : afea32b87`, The Great Wave

## Verdict

```text
LOG_CLEANUP_3 = PASS
BATCH_DIAGNOSTICS_IN_SCOPE = 14
BATCH_DIAGNOSTICS_PROVEN_FIXABLE = 12
BATCH_DIAGNOSTICS_PATCHED = 12
BATCH_DIAGNOSTICS_SKIPPED = 2
BATCH_DIAGNOSTICS_RUNTIME_CLEARED = 12
```

Les 11 migrations de modifier de loi et l'unique clé de technologie sont prouvées, corrigées et validées dans une seule génération runtime humaine. Les deux diagnostics Dreyfus restent intacts comme prévu : leur cause réelle se trouve dans un fichier de template hors périmètre.

## Préflight Git

```text
BRANCH = post-2.3.0-log-cleanup
HEAD = 2b3d8e141dbf4dedbd5b2f792cb570a869313ae9
HEAD_SUBJECT = Align VOC prosperity modifier with Victoria 3 1.13
WORKTREE_BEFORE = CLEAN
INDEX_BEFORE = EMPTY
LOG_CLEANUP_2_COMMITTED = YES
```

Le préflight correspond exactement à l'état demandé. Aucun changement préexistant n'a été supprimé, déplacé ou écrasé.

## Baseline et périmètre

LOG-CLEANUP-1 classait 15 identités `FORK_ATTRIBUTABLE_FIXABLE`. LOG-CLEANUP-2 a corrigé et validé `API_COUNTRY_CONVOYS_CAPACITY_MULT = 1`. Les 14 identités restantes sélectionnées ici sont :

| Famille | Diagnostics | Chemins | Gate |
|---|---:|---:|---|
| `LEGACY_LAW_ENACTMENT_MODIFIER` | 11 | 5 | `PROVEN_BOUNDED_FIX` |
| `API_HAS_TECHNOLOGY_RESEARCHED` | 1 | 1 | `PROVEN_BOUNDED_FIX` |
| `API_CREATE_CHARACTER` — Dreyfus seulement | 2 | 1 | `NO_SAFE_ATOMIC_FIX` |

Les trois `create_character` du Caucase autour des lignes historiques 730, 759 et 1039 ne participent jamais à ce lot.

## Family A — modifier d'enactment

### Registre 1.13.9

`country_law_enactment_time_mult` est absent des définitions vanilla 1.13.9. Son successeur fonctionnel est enregistré dans `common/modifier_type_definitions/00_modifier_types.txt:1110` :

```text
country_law_enactment_speed_mult = {
    decimals = 0
    color = good
    percent = yes
}
```

La localisation vanilla le décrit comme une augmentation ou diminution de la vitesse des enactments législatifs. Il conserve le scope `country` et une valeur proportionnelle, mais la variable mesure désormais la vitesse plutôt que le temps : le signe doit donc être inversé pour préserver l'effet favorable ou défavorable.

### Preuve homologue exacte

Les objets identiques des deux fichiers d'amendments vanilla fournissent trois migrations officielles directes :

| Objet | Fork legacy | Vanilla 1.13.9 |
|---|---|---|
| premier amendment de `00_amendments_content_04.txt` | `time_mult = 0.10` | `speed_mult = -0.10` |
| `amendment_geheime_staatskonferenz_kolowrat` | `time_mult = 0.25` | `speed_mult = -0.25` |
| `amendment_geheime_staatskonferenz` | `time_mult = 0.20` | `speed_mult = -0.20` |

La règle commune prouvée est donc :

```text
country_law_enactment_time_mult = X
-> country_law_enactment_speed_mult = -X
```

Les usages vanilla positifs et négatifs de `country_law_enactment_speed_mult` dans les legitimacy levels, static modifiers, interest-group traits et power blocs confirment la même orientation : positif accélère, négatif ralentit.

### Application

Les 11 occurrences conservent leur magnitude et inversent leur signe. Les anciennes valeurs négatives `-0.45`, `-0.25` et `-0.10` deviennent des bonus de vitesse positifs ; les anciennes valeurs positives deviennent des pénalités de vitesse négatives.

```text
DIAGNOSTICS_BEFORE = 11
STATIC_OCCURRENCES_BEFORE = 11
STATIC_OCCURRENCES_AFTER = 0
PATCHED_DIAGNOSTICS = 11
SKIPPED_DIAGNOSTICS = 0
SKIP_REASON = NONE
```

## Family B — technologie de l'objectif Hegemon

Le trigger `has_technology_researched` reste valide en 1.13.9. Le PostValidate échoue sur son objet droit : la technologie legacy `dreadnought` n'est plus la clé attendue.

L'homologue vanilla exact de `je_increase_technology` conserve les trois triggers, avec une seule différence pertinente :

```text
has_technology_researched = dreadnought
-> has_technology_researched = dreadnought_tech
```

`bolt_action_rifles` et `malaria_prevention` restent inchangés. Aucun fichier de technologie ni document de recherche n'est modifié.

```text
DIAGNOSTICS_BEFORE = 1
STATIC_OCCURRENCES_BEFORE = 1
STATIC_OCCURRENCES_AFTER = 0
PATCHED_DIAGNOSTICS = 1
SKIPPED_DIAGNOSTICS = 0
SKIP_REASON = NONE
```

## Family C — créations Dreyfus

Les blocs des lignes baseline 84 et 244 emploient déjà exactement la forme vanilla 1.13.9 : `create_character`, `template`, `save_scope_as` et `on_created` sont homologues. Le troisième bloc Zola de ce fichier utilise la même structure sans produire le diagnostic ciblé.

La génération fraîche disponible avant le lot donne une cause plus précise pour les deux échecs :

```text
Invalid HQ region_france in events/agitators_events/dreyfus_events.txt:84
Invalid HQ region_france in events/agitators_events/dreyfus_events.txt:244
```

La valeur fautive n'est pas écrite dans l'event. Elle provient de `common/character_templates/dreyfus_template.txt`, où les templates Dreyfus et Esterhazy utilisent `hq = region_france`. La vanilla 1.13.9 utilise `hq = region_western_europe` et ajoute aussi des `home_region`. Ce fichier de template n'est pas autorisé dans LOG-CLEANUP-3.

Modifier les blocs `create_character` identiques à la vanilla ne corrigerait pas la dépendance. Importer les personnages en ligne ou ouvrir le template élargirait le périmètre et exigerait une décision sur HQ et home region. La gate est donc rejetée sans bloquer les familles A/B.

```text
DIAGNOSTICS_BEFORE = 2
STATIC_OCCURRENCES_BEFORE = 2
STATIC_OCCURRENCES_AFTER = 2
PATCHED_DIAGNOSTICS = 0
SKIPPED_DIAGNOSTICS = 2
SKIP_REASON = ROOT_CAUSE_IN_UNAUTHORIZED_CHARACTER_TEMPLATE
DREYFUS_EVENT_SHA256_BEFORE = 14288ECEBC084C381FE4A5550B586A6B5DB87AA1CBE84C6FF4423770A7D5DEC5
DREYFUS_EVENT_SHA256_AFTER = 14288ECEBC084C381FE4A5550B586A6B5DB87AA1CBE84C6FF4423770A7D5DEC5
```

## Correctif consolidé

| Fichier | Diagnostics corrigés | SHA-256 avant | SHA-256 après |
|---|---:|---|---|
| `common/amendments/00_amendments_content_04.txt` | 2 | `A10A686E73E57F08826B2F1DB033A69E3CD0E8E89E3128512AD26617F8FC4A1B` | `13A8A03E127FB0C8D03255F4B6909363A1E161021BE41DC9C8DBF35B89113FBF` |
| `common/amendments/00_amendments_historical_04.txt` | 1 | `9A3DCDB444CC6AE2F47365E59BB2FE725BF60C96093968F94920667BC66599BD` | `9114B56FB7C57D054E02F9335E44F12745607BCA65CB76587A55DC9F4A8B857F` |
| `common/amendments/00_amendments_modded_76.txt` | 1 | `55518F227F7095DF620EEC2CB8C27A603F24FFBC286FC3BE6347A01D0C71ED3A` | `742B1A1DFC988AF5BC6B37F626D6A89A95BB1C05F0B8314D39B89991B1D72A57` |
| `common/laws/00_inject_laws.txt` | 1 | `1993A8160673ECAD1D7B6C1F2D7F1AA5A4340A6826E6BF1EB9F92FE7970CD566` | `AF662E95681F86ADD0CF4A190756009A79A235B6529DA6462B08E8A5D587F42D` |
| `common/static_modifiers/76mod_modifiers.txt` | 6 | `DCD4B0768EF778E8191DDD59D40C374128901E084D6446323EF5DA8CEC5B2FCA` | `CDE96556B1EDD89800E8DEB01C8843F300E537A09B4CBBD1E8F4CBF5927FE813` |
| `common/journal_entries/00_player_objectives_hegemon.txt` | 1 | `759947552094A1C9230E2BB2A1CBC5B7058AE6D42EF7161FCD5C41660384E6B6` | `78DE7DB850AFB06CA37C923C32507CBB3B00A5B252A9194A8245404BDA71ACF6` |

```text
GAMEPLAY_CHANGED_FILES = 6
GAMEPLAY_CHANGED_HUNKS = 11
GAMEPLAY_INSERTIONS = 12
GAMEPLAY_DELETIONS = 12
```

## Validation statique

```text
GIT_DIFF_CHECK = PASS
LAW_LEGACY_GAMEPLAY_OCCURRENCES_AFTER = 0
LAW_MODERN_OCCURRENCES_IN_TARGET_FILES = 11
HEGEMON_DREADNOUGHT_LEGACY_OCCURRENCES_AFTER = 0
HEGEMON_DREADNOUGHT_TECH_OCCURRENCES_AFTER = 1
CAUCASUS_CREATE_CHARACTER_TOUCHED = NO
TECH_TREE_FILES_CHANGED = 0
SEMANTIC_CREATE_CHARACTER_FILES_CHANGED = 0
UNRELATED_GAMEPLAY_FILES_CHANGED = 0
INDEX = EMPTY
```

La matrice occurrence par occurrence est `LOG_CLEANUP_3_PATCH_MATRIX.csv`.

## Runtime humain consolidé

L'opérateur humain a lancé Victoria 3, atteint le menu principal puis quitté proprement le jeu. Codex n'a pas lancé le jeu. La génération fraîche commence à `21:12:41` et se termine à `21:18:33` le 14 août 2026.

`error.log` a tourné une fois pendant cette session. Les diagnostics ont donc été agrégés depuis les deux segments courants `error.1.log` et `error.log`; les rotations plus anciennes et `debug.2.log` ont été exclues.

```text
VICTORIA_3_VERSION = release/1.13.9 : afea32b87
THE_GREAT_WAVE_MOUNTED = YES
TARGET_FORK_DECLARED = YES
TARGET_FORK_MOUNTED = YES
OTHER_1776_BUILD_MOUNTED = NO
TARGET_FORK_PATH = C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork
SYSTEM_LOG_SHA256 = 64E93779B7ECF93DA362555945A79229995C1D9DAD1CD25A535AFEB47635D612
DEBUG_1_LOG_SHA256 = 32915B69199FE2A86962FB24096F1609A9508E02AE2147B7E7E2E1B999DCA9C2
DEBUG_LOG_SHA256 = 7C2BA6CC194195D0BC7C7C65AAE1AE2D3D4C5DA113164307EFB17FDA0472A094
ERROR_1_LOG_SHA256 = 03322931ADCFF7ADACFB548F3BE79A06E404B14F6DD4A75118C653E4F2503DF9
ERROR_LOG_SHA256 = 5AB5B6341DE209392F2BA0755BF1A00F75C0155AD862608A9CA85DB0C1170195
GAME_LOG_SHA256 = C8FF41F055942E84F0F156B6438304E64D1961399293F9552B7AB78A0FCD08F1
```

Les 11 erreurs de modifier legacy et le PostValidate de l'objectif Hegemon ont disparu. Aucun diagnostic ne cite `country_law_enactment_speed_mult` ni `dreadnought_tech`. Aucun des six fichiers corrigés ne produit de nouveau diagnostic attribuable.

Les deux diagnostics Dreyfus restent présents aux lignes 84 et 244 avec `Invalid HQ region_france`, exactement conformément à la gate rejetée. Les trois diagnostics Caucase protégés restent présents aux lignes 730, 759 et 1039 ; ils n'ont pas été modifiés.

```text
LAW_ENACTMENT_DIAGNOSTICS_BEFORE = 11
LAW_ENACTMENT_DIAGNOSTICS_AFTER = 0
HAS_TECHNOLOGY_DIAGNOSTICS_BEFORE = 1
HAS_TECHNOLOGY_DIAGNOSTICS_AFTER = 0
DREYFUS_CREATE_CHARACTER_DIAGNOSTICS_BEFORE = 2
DREYFUS_CREATE_CHARACTER_DIAGNOSTICS_AFTER = 2
CAUCASUS_CREATE_CHARACTER_DIAGNOSTICS_AFTER = 3
NEW_ATTRIBUTABLE_DIAGNOSTICS = 0
```

## Protections Git

```text
STAGED_FILES = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
```

## Résultat final

```text
LOG_CLEANUP_3 = PASS
BRANCH = post-2.3.0-log-cleanup
HEAD = 2b3d8e141dbf4dedbd5b2f792cb570a869313ae9
BATCH_DIAGNOSTICS_IN_SCOPE = 14
BATCH_DIAGNOSTICS_PROVEN_FIXABLE = 12
BATCH_DIAGNOSTICS_PATCHED = 12
BATCH_DIAGNOSTICS_SKIPPED = 2
BATCH_DIAGNOSTICS_RUNTIME_CLEARED = 12
LAW_ENACTMENT_DIAGNOSTICS_BEFORE = 11
LAW_ENACTMENT_DIAGNOSTICS_AFTER = 0
HAS_TECHNOLOGY_DIAGNOSTICS_BEFORE = 1
HAS_TECHNOLOGY_DIAGNOSTICS_AFTER = 0
DREYFUS_CREATE_CHARACTER_DIAGNOSTICS_BEFORE = 2
DREYFUS_CREATE_CHARACTER_DIAGNOSTICS_AFTER = 2
CAUCASUS_CREATE_CHARACTER_TOUCHED = NO
NEW_ATTRIBUTABLE_DIAGNOSTICS = 0
GAMEPLAY_CHANGED_FILES = 6
GAMEPLAY_CHANGED_HUNKS = 11
DOCUMENTATION_FILES_CREATED = 2
TECH_TREE_FILES_CHANGED = 0
STAGED_FILES = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
REMAINING_FORK_ATTRIBUTABLE_FIXABLE = 2
NEXT_PHASE = LOG-CLEANUP-4-POST-FIXABLE-FRESH-REINDEX
```

## Suite exclusive

Après validation du runtime consolidé :

```text
NEXT_PHASE = LOG-CLEANUP-4-POST-FIXABLE-FRESH-REINDEX
```

LOG-CLEANUP-4 n'est pas commencé.
