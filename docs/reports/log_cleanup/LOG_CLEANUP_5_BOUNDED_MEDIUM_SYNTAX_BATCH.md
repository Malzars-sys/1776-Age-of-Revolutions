# LOG-CLEANUP-5 — Bounded & medium syntax batch

## État

`STATIC_AUDIT = PASS`

`RUNTIME = PASS`

LOG-CLEANUP-5 audite indépendamment quatre diagnostics répartis dans deux familles. La gate canton passe et son correctif borné est appliqué. La gate Interest Group échoue proprement : aucune migration sémantiquement équivalente n'est démontrée, donc `00_landowners.txt` reste inchangé.

## Prévol

- branche : `post-2.3.0-log-cleanup`
- HEAD initial : `992bbc425df648548a3cbdb3ddeec2fd77a43db7`
- commit HEAD : `992bbc4 Reindex post-fixable release diagnostics`
- worktree initial : propre
- index initial : vide
- baseline LOG-CLEANUP-4 : 327 identités
- erreurs fork connues avant : 48
- attribution en attente : 5

## Gate A — variables de canton

`FLAG_CANTON_SAFE_FIX = YES`

### Preuve

Le bloc `DENNOR` de `common/flag_definitions/07_NM_Flags.txt` provient sans modification de contenu du commit d'import initial `b602804`. Sa ligne 186 réutilisait :

```text
@canton_scale_denmark_x
@canton_scale_denmark_y
```

Vanilla 1.13.9 définit dans `common/flag_definitions/00_flag_definitions.txt` :

```text
@coa_width = 768
@coa_height = 512
@canton_scale_denmark_x = @[ ( 220 / coa_width ) + 0.001 ]
@canton_scale_denmark_y = @[ ( 220 / coa_height ) + 0.001 ]
```

Le bloc vanilla `DEN` emploie ces variables dans la même unité de parsing. La génération LOG-CLEANUP-4 démontre que leur réutilisation depuis `07_NM_Flags.txt` n'est pas résolue entre fichiers. Définir les mêmes noms localement élargirait inutilement le fichier et pourrait introduire une collision future.

La substitution locale exacte est donc :

```text
overlord_canton_scale = { @[ ( 220 / 768 ) + 0.001 ] @[ ( 220 / 512 ) + 0.001 ] }
```

Les valeurs mathématiques sont inchangées :

- X = `0.287458333333333...` ;
- Y = `0.4306875`.

La syntaxe `@[ ... ]` à l'intérieur de `overlord_canton_scale` est attestée dans les définitions vanilla 1.13.9. Le patch change une seule ligne du bloc `DENNOR`, ne dépend plus d'une variable inter-fichiers et ne touche aucune autre définition de drapeau.

### Compteurs statiques

- `FLAG_DIAGNOSTICS_BEFORE = 2`
- `FLAG_STATIC_LEGACY_REFERENCES_BEFORE = 2`
- `FLAG_STATIC_LEGACY_REFERENCES_AFTER = 0`
- expressions locales attendues présentes : 2/2

Le runtime frais confirme `FLAG_DIAGNOSTICS_AFTER = 0`.

## Gate B — chances de leader Interest Group

`IG_LEADER_CHANCE_SAFE_MIGRATION = NO`

### Sémantique historique établie

- `OLD_COMMANDER_KEY_SEMANTICS` : probabilité que le commandant le plus populaire appartenant à l'IG prenne sa direction lors d'un changement ;
- `OLD_EXECUTIVE_KEY_SEMANTICS` : probabilité que l'executive le plus populaire appartenant à l'IG prenne sa direction lors d'un changement ;
- `OLD_SCOPE` : racine Interest Group, avec `scope:character` documenté comme le commandant ou l'executive le plus populaire ;
- `OLD_VALUES` : commander `0.5`, multiplié par `ig_commander_leader_chance_mult`; executive `0.1`.

Le blame et les recherches `git log -S` rattachent les deux blocs au commit d'import initial `b602804`; aucun commit ultérieur du dépôt ne documente une migration.

### Système 1.13.9

Les clés `commander_leader_chance` et `executive_leader_chance` n'existent plus dans l'installation Victoria 3 1.13.9. Les huit définitions vanilla d'Interest Groups emploient un système de poids comprenant :

- `commander_leader_weight` ;
- `magnate_leader_weight` ;
- `executive_leader_weight`.

Pour les landowners vanilla, les valeurs sont respectivement `1.5`, `5.0` et `0.5`, avec une condition japonaise supplémentaire sur le poids magnate. Les commentaires 1.13.9 décrivent un multiplicateur de poids appliqué à un candidat approprié sélectionné depuis le character pool, et non une probabilité de prise de direction par le personnage le plus populaire.

Un simple renommage conserverait des valeurs `0.5` et `0.1` dans un algorithme différent. Copier uniquement les deux valeurs vanilla omettrait le troisième type de candidat et sa logique japonaise. Copier tout le bloc moderne dépasserait les deux diagnostics sélectionnés et imposerait une décision de gameplay plus large. Les valeurs ne sont donc pas convertibles avec une équivalence démontrée.

### Décision

Les deux diagnostics IG sont différés. Aucun token n'est supprimé et aucun octet de `common/interest_groups/00_landowners.txt` n'est modifié.

- `IG_DIAGNOSTICS_BEFORE = 2`
- `IG_LEGACY_KEYS_BEFORE = 2`
- `IG_LEGACY_KEYS_AFTER = 2`
- `IG_DIAGNOSTICS_AFTER = 2`, famille non patchée et reproduite comme attendu

## Patch et validation statique

Fichier gameplay modifié :

- `common/flag_definitions/07_NM_Flags.txt` — un hunk, une insertion, une suppression.

Fichiers gameplay non modifiés :

- `common/interest_groups/00_landowners.txt` ;
- tous les fichiers hors périmètre.

Contrôles exécutés :

- `git diff --check` : PASS ;
- références canton héritées dans le fichier cible : 2 → 0 ;
- expressions locales exactes : 0 → 2 ;
- clés IG : 2 → 2 ;
- reformatage global : aucun ;
- index Git : vide ;
- staging/commit/push : aucun.

## Runtime consolidé

Codex n'a pas lancé Victoria 3. L'opérateur humain a effectué un lancement unique et indique être allé jusqu'à l'écran de choix des Pays-Bas avant de quitter.

### Provenance

- session locale : `2026-08-14 21:55:43` à `22:08:05` (`Europe/Paris`) ;
- version : `release/1.13.9 : afea32b87` ;
- The Great Wave : monté ;
- mod : `Age of revolution /Fork` depuis `1776_Age_of_Revolutions_fork` ;
- autre mod 1776 : aucun dans la liste montée ;
- sortie normale : `Quit from inside game`, transition `Game->Empty`, un joueur supprimé.

Hashes SHA-256 des segments retenus :

| Segment | SHA-256 |
| --- | --- |
| `code_revisions.log` | `77286121F4183BEA38E4D1AD7D75B2A8379AA249A163E6FFDE4352E1041EAC00` |
| `system.log` | `5EFD5A6576C3177CB2F6CA169CF2F8A6A6591759BAC9657ED5F8BF29670DCB31` |
| `debug.1.log` | `631A1D32F3F37FE02017C53B24DFC58E7522802302E81C45802C215AD30BB866` |
| `debug.log` | `C3CA834A6A833758A89A69545240016054AE54EA6F7E4FF5A50DCAFCC04D5CBB` |
| `error.5.log` | `9452350C652D65192E7B43E44192B340ABC0D65BE2713D21DDD27B0C6D7F8F74` |
| `error.4.log` à `error.1.log` | `7349EE78E2AF73BF448E2D8B7E74BA7D6957A7BF5257D441578F41DCBA50BEEF` chacun |
| `error.log` | `A3C56C506E4E4314977BF7F3147B1C980564D8BD153132A3E30E63D738712A18` |
| `game.5.log` à `game.1.log` | `7349EE78E2AF73BF448E2D8B7E74BA7D6957A7BF5257D441578F41DCBA50BEEF` chacun |
| `game.log` | `206D4895F1A2B9A4AD602DA245AAD2FB456F17C4F433503BD0E3D3429E8FAE10` |

Toutes les rotations de cette session ont été examinées.

### Résultats ciblés

| Diagnostic | Avant | Après | Résultat |
| --- | ---: | ---: | --- |
| `Malformed token: @canton_scale_denmark_x` | 1 | 0 | CLEARED |
| `Malformed token: @canton_scale_denmark_y` | 1 | 0 | CLEARED |
| `Unexpected token: commander_leader_chance` | 1 | 1 | DEFERRED_EXPECTED |
| `Unexpected token: executive_leader_chance` | 1 | 1 | DEFERRED_EXPECTED |

Aucune ligne de diagnostic ne référence `common/flag_definitions/07_NM_Flags.txt`.

Le reparse parser/PostValidate produit 325 identités et 357 occurrences. Les 325 identités sont toutes exactes dans LOG-CLEANUP-4 ; les deux seules identités LOG-CLEANUP-4 absentes sont les deux cantons. Il n'existe donc aucune nouvelle identité parser/PostValidate attribuable au patch.

### Couverture étendue de l'écran de sélection

La progression jusqu'à l'écran de sélection a aussi reproduit les familles runtime absentes de la session menu de LOG-CLEANUP-4 :

- 121 identités achievement externes ;
- 113 identités country-law ;
- cinq identités de comparaison/scope runtime.

Quatre identités de comparaison/scope étaient déjà connues. Une cinquième identité apparaît à `common/ai_strategies/00_default_strategy.txt:2023` avec `Invalid right side during comparison 'sr'` (3 occurrences). Elle appartient au même système AI/strategic-region que la phase suivante, n'a aucun lien de chemin, de token ou de causalité avec le patch canton et n'est pas comptée comme régression de LOG-CLEANUP-5. Elle devra être absorbée par le reindex de LOG-CLEANUP-6.

Sur toute la taxonomie LOG-CLEANUP-1, cette génération contient 564 identités et 16 625 occurrences. Ce total plus élevé reflète la couverture country-selection et n'invalide pas la fermeture ciblée.

## Compteurs finaux

- `BATCH_DIAGNOSTICS_IN_SCOPE = 4`
- `BATCH_DIAGNOSTICS_PATCHED = 2`
- `BATCH_DIAGNOSTICS_DEFERRED = 2`
- `BATCH_DIAGNOSTICS_RUNTIME_CLEARED = 2`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0`
- `KNOWN_FORK_ERRORS_REQUIRING_CORRECTION_AFTER = 46`

Le compteur 46 applique l'arithmétique demandée à la baseline LOG-CLEANUP-4 : 48 moins les deux cantons validés. L'identité AI découverte par couverture étendue est documentée séparément et sera intégrée à la famille/reindex de LOG-CLEANUP-6, sans réécrire rétroactivement la baseline 327.

La roadmap restante compte six phases probables : audit/design IG, migration AI, sémantique character/template, audit modifier, reproduction country-law et reindex/QA final. Estimation : minimum 5, probable 6, maximum 8.

`NEXT_PHASE = LOG-CLEANUP-6-AI-STRATEGY-SEMANTIC-MIGRATION` n'est pas commencée.
