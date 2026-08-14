# LOG-CLEANUP-6 — AI strategy semantic migration

## État

`STATIC_AUDIT = PASS`

`RUNTIME = PASS`

Le lot AI consolidé traite les 39 diagnostics de la baseline et la nouvelle identité runtime `:2023`. Les trois gates passent sur preuve locale 1.13.9. Aucun bloc vanilla complet n'est importé : les conditions, valeurs et commentaires propres au fork sont conservés, seuls les sélecteurs obsolètes sont migrés.

## Prévol

- branche : `post-2.3.0-log-cleanup` ;
- HEAD initial : `13ec0dc23cc8a767a5ae4bf3d3ad6b49bcd1eea6` ;
- commit HEAD : `13ec0dc Fix Denmark-Norway canton scale parsing` ;
- worktree initial : propre ;
- index initial : vide ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 47` ;
- fichier gameplay autorisé unique : `common/ai_strategies/00_default_strategy.txt`.

## Historique et structure legacy

Le fichier cible et les trois structures concernées proviennent du commit d'import initial `b602804`. Les recherches `git log -S"region_andes"`, `git log -S"has_port"` et les blames ciblés ne montrent aucune migration ultérieure dans le dépôt.

Pour `strategic_region_scores` :

- `OLD_BLOCK_TYPE = strategic_region_scores keyed scripted-value table` ;
- `OLD_REGION_KEY_ROLE = clé de sélection de l'ancienne strategic region` ;
- `OLD_VALUE_SEMANTICS = score additif calculé par un corps conditionnel propre à chaque région` ;
- `OLD_SCOPE = pays AI en racine; région implicitement sélectionnée par la clé` ;
- `OLD_AI_PURPOSE = pondérer le maintien d'intérêts géographiques selon journaux, rang, technologie, doctrine et objectifs historiques`.

La 1.13.9 remplace cette table par une valeur unique initialisée à zéro et évaluée pour `scope:region`. Les conditions modernes utilisent soit un objet `sr:` encore valide, soit un test géographique. Le fichier vanilla `common/geographic_regions/06_old_strategic_regions.txt` fournit explicitement les empreintes des anciennes régions après leur consolidation.

## Gate strategic regions

`STRATEGIC_REGION_MIGRATION_SAFE = YES`

Les 32 mappings sont détaillés dans `LOG_CLEANUP_6_AI_MIGRATION_MATRIX.csv`.

Méthode appliquée :

```text
strategic_region_scores = {
    value = 0
    if = {
        limit = { scope:region = <objet ou empreinte prouvée> }
        <corps de score legacy inchangé>
    }
}
```

Deux catégories de preuve sont utilisées :

- région stratégique 1.13.9 inchangée : `scope:region = sr:region_*` ;
- région remaniée : `scope:region = { is_in_geographic_region = geographic_region_*_old }`.

Chaque objet a été vérifié physiquement dans les définitions 1.13.9. Les quatre régions stratégiques sud-américaines sont explicitement documentées par vanilla comme inchangées. Pour les régions remaniées, les objets `_old` conservent la liste de state regions legacy. Cette approche évite d'inventer une nouvelle géographie et ne copie pas les nouveaux scores vanilla, dont plusieurs valeurs diffèrent du fork.

Les 32 corps de score préexistants sont conservés : Caucasian War, Hawaii, Sakoku, Scramble for Africa, unifications allemande/italienne, Schleswig-Holstein, Great Game, Opium Wars, Monroe Doctrine et Reconquista.

- `STRATEGIC_REGION_DIAGNOSTICS_BEFORE = 32`
- `STRATEGIC_REGION_PATCHED = 32`
- `STRATEGIC_REGION_DEFERRED = 0`
- anciennes clés top-level après patch : 0

## Gate has_port

`HAS_PORT_MIGRATION_SAFE = YES`

Les sept occurrences sémantiques du fichier cible ont un homologue exact dans le même bloc vanilla 1.13.9 :

- pays courant ou pays explicitement scopé : `has_port_country` — 6 diagnostics ;
- état cible : `has_port_state` — 1 diagnostic.

Les intentions sont préservées : disponibilité maritime des deux pays dans le Great Game, absence de port dans un état non adjacent, et capacité du pays à demander des navires dans les quatre stratégies de biens.

- `HAS_PORT_DIAGNOSTICS_BEFORE = 7`
- `HAS_PORT_PATCHED = 7`
- `HAS_PORT_DEFERRED = 0`
- ancien trigger `has_port` dans le fichier cible après patch : 0
- triggers modernes ciblés présents : 7

Les deux `API_HAS_PORT` classés `ALREADY_ACCOUNTED_FOR` sont dans `events/meiji_restoration.txt`, pas dans le fichier AI cible. Ils restent hors lot et inchangés. `RECLASSIFICATION_REQUIRED = NO`.

## Gate nouvelle identité runtime

`NEW_SR_RUNTIME_IDENTITY_SAME_ROOT_CAUSE = YES`

L'identité `Invalid right side during comparison 'sr'` à la ligne runtime 2023 vient de :

```text
scope:target_state = {
    region = sr:region_manchuria
}
```

`sr:region_manchuria` n'existe plus comme strategic region 1.13.9. Le bloc vanilla homologue utilise :

```text
is_in_geographic_region = geographic_region_manchuria_old
```

Le scope reste un état et l'empreinte géographique est celle de l'ancienne Manchuria. La correction est exacte.

L'audit a aussi rattaché l'identité runtime historique très répétée autour de l'ancienne ligne 5078 à un autre comparateur Manchuria dans le même fichier. Les homologues vanilla prouvent deux migrations :

- état dans l'ancienne Manchuria : `geographic_region_manchuria_old` ;
- sélection Japan/Manchuria dans le système moderne : `sr:region_northeast_asia`.

Ces comparateurs directement liés ont été migrés afin de ne pas laisser la cause racine active derrière les 40 identités opérationnelles.

- `NEW_SR_RUNTIME_DIAGNOSTICS_BEFORE = 1`
- `NEW_SR_RUNTIME_PATCHED = 1`
- `NEW_SR_RUNTIME_DEFERRED = 0`
- références `sr:region_manchuria` et `sr:region_japan` après patch : 0

## Portée du patch

- `TARGET_FILE_SHA256_BEFORE = 15704A99428C960B65F2F074ACB8508E66A9D5AA9B8F49436C0EC17569E2D139`
- `TARGET_FILE_SHA256_AFTER = ACD69F3AA69BB61DA79CD66734D2868DBEEA92E472AF785914A39603192A7515`
- `GAMEPLAY_CHANGED_FILES = 1`
- `GAMEPLAY_CHANGED_HUNKS = 44`
- `GAMEPLAY_INSERTIONS = 77`
- `GAMEPLAY_DELETIONS = 44`

Les 44 hunks correspondent aux sept substitutions `has_port`, aux sélecteurs des 32 entrées, à l'initialisation de la valeur, et aux comparateurs Manchuria/Japan directement homologues. Aucun reformatage global n'est effectué.

## Validation statique

- équilibre des accolades hors commentaires : 2284 ouvrantes / 2284 fermantes ;
- anciennes clés régionales top-level : 32 → 0 ;
- ancien trigger exact `has_port` : 7 → 0 ;
- triggers `has_port_country` / `has_port_state` ciblés : 0 → 7 ;
- sélecteurs régionaux migrés : 32/32 ;
- références invalides `sr:region_manchuria` / `sr:region_japan` : 4 → 0 ;
- `git diff --check` : PASS ;
- fichiers gameplay modifiés : le fichier autorisé uniquement ;
- index Git : vide ;
- staging/commit/push : aucun.

## Références statiques latentes hors lot

L'audit typé complet du fichier trouve encore 49 références `sr:` vers six anciennes régions qui n'existent plus comme strategic regions 1.13.9 :

- `region_bombay` : 10 ;
- `region_punjab` : 9 ;
- `region_madras` : 8 ;
- `region_bengal` : 8 ;
- `region_central_india` : 8 ;
- `region_persia` : 6.

Ces références n'avaient produit aucune identité dans les runtimes LOG-CLEANUP-1/4/5 retenus pour ce lot et leurs blocs ne font pas partie des 40 diagnostics autorisés. Elles n'ont donc pas été patchées silencieusement. Le runtime LOG-CLEANUP-6 prolongé jusqu'au 1er janvier 1777 en a matérialisé huit identités distinctes. Elles sont comptées dans `AI_FILE_NEW_DIAGNOSTICS` et `NEW_CONFIRMED_FORK_ERRORS_DISCOVERED`, avec un lot AI de suivi avant toute phase IG.

## Reindex AI local — référence avant runtime

Le runtime LOG-CLEANUP-5 contenait dans le fichier AI :

- 32 erreurs parser de clés régionales ;
- 7 erreurs parser `has_port` ;
- l'identité runtime stratégique historique autour de la ligne 5078 ;
- la nouvelle identité runtime autour de la ligne 2023 ;
- 1 `is_building_type` intentionnel déjà classé.

`AI_FILE_DIAGNOSTICS_BEFORE = 42` sur la taxonomie complète locale. Le compteur opérationnel du lot reste 40 conformément au brief : 39 baseline + 1 nouvelle identité. L'identité historique 5078 partage la cause racine des migrations et le diagnostic intentionnel n'est pas ajouté au compteur correctif.

## Runtime humain et provenance

Codex n'a pas lancé Victoria 3. L'opérateur a chargé une nouvelle partie avec les Pays-Bas et l'a laissée tourner jusqu'au tick `1777.1.1`, confirmé dans `dedicated_server.log`, avant une fermeture propre.

- début de session : `2026-08-14 22:27:19 +02:00` ;
- fin de session : `2026-08-14 22:36:59 +02:00` ;
- build : `release/1.13.9 : afea32b87` ;
- DLC The Great Wave : monté ;
- mod monté : `Age of revolution /Fork|.../1776_Age_of_Revolutions_fork` ;
- autre build 1776 monté : aucun ;
- rotation exclue : `debug.1.log`, terminée à 22:08:05 et appartenant au runtime précédent ;
- rotations courantes analysées : `debug.log`, `error.5.log` à `error.log`, `game.5.log` à `game.log`, `dedicated_server.log`, `system.log` et `code_revisions.log`.

Empreintes principales :

| Segment | Octets | SHA-256 |
|---|---:|---|
| `debug.log` | 445018 | `6C454B63FAB94EEDE8D3B5FE199BDE818EBFCFC7F198B87B90C02FD17ADAFCDE` |
| `error.5.log` | 524215 | `B560B8EDF373EFD9EF20BA0013299ABC79ADEABAE083617D07124DB00E866E2B` |
| `error.4.log` | 524098 | `B2D90AE0CBB9377A6DA647D0AD1CC7EC8C1663C9C415EF5AE48220E488E708AB` |
| `error.3.log` | 524105 | `845FD7CAC5F94B2D9B78AB942AD7B781E642E0A3C0D24ED6252C9E66B20552C4` |
| `error.2.log` | 524113 | `72521439D48AF4210FA2568421B517E31F48520835A5BF1B44481FEA072BE767` |
| `error.1.log` | 524198 | `21214A79FD3488A59D763E4823F7DEE714D042A509D16A7A22863556619A72BA` |
| `error.log` | 208032 | `42C6822C4DFDB72AFB2B44AC4099794DDD2B83B869492CAF545B081D7C74EA89` |
| `dedicated_server.log` | 102184 | `10A796A008B416E67E20A1DE3918D65CFBFC98604657C89DE8926BF4D35A8B58` |

## Résultats runtime ciblés

Les 40 diagnostics autorisés sont absents du runtime frais :

- anciennes clés parser de strategic regions : `32 → 0` ;
- sept anciens triggers AI `has_port` : `7 → 0` ;
- nouvelle identité Manchuria autour de l'ancienne ligne 2023 : `1 → 0` ;
- diagnostics attribuables aux nouvelles structures `if`/`scope:region`, `has_port_country`, `has_port_state` ou `geographic_region_manchuria_old` : 0.

Les deux `has_port` de `events/meiji_restoration.txt`, déjà classés `ALREADY_ACCOUNTED_FOR`, se reproduisent et restent hors lot. Le `PostValidate` intentionnel de `is_building_type` se reproduit à la nouvelle ligne 5119 ; il ne constitue ni une nouvelle identité ni une erreur attribuable au patch.

## Reindex AI local — résultat

Huit nouvelles identités distinctes, pour 96 occurrences, sont apparues dans les références legacy statiques laissées hors lot :

| Ligne runtime | Référence | Occurrences |
|---:|---|---:|
| 1482 | `sr:region_madras` | 12 |
| 1483 | `sr:region_bombay` | 12 |
| 1484 | `sr:region_bengal` | 12 |
| 1485 | `sr:region_central_india` | 12 |
| 1551 | `sr:region_persia` | 9 |
| 1553 | `sr:region_bombay` | 9 |
| 1554 | `sr:region_punjab` | 9 |
| 2836 | `sr:region_persia` | 21 |

Le message est dans chaque cas `Invalid right side during comparison 'sr'`. Ces lignes existaient avant le patch, appartiennent aux 49 références invalides déjà inventoriées et n'utilisent aucune des structures ajoutées par cette phase. `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_AI_PATCH = 0`.

- `AI_FILE_DIAGNOSTICS_BEFORE = 42` ;
- `AI_FILE_DIAGNOSTICS_AFTER = 9` (8 nouvelles identités legacy + 1 diagnostic intentionnel déjà classé) ;
- `AI_FILE_NEW_DIAGNOSTICS = 8` ;
- `AI_DIAGNOSTICS_CLEARED = 40` ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 47 - 40 + 8 = 15`.

Les diagnostics historiques `country_law_manager` ne se sont pas reproduits dans cette session : `COUNTRY_LAW_DIAGNOSTICS_REPRODUCED = 0/113`. Ils restent réservés à leur audit dédié et ne sont pas considérés corrigés.

## Conclusion et suite

`LOG_CLEANUP_6 = PASS` : le lot sémantique autorisé ferme ses 40 diagnostics sans régression attribuable. Les huit identités nouvellement exercées imposent un lot AI groupé supplémentaire avant le design IG. La roadmap probable contient désormais six phases : résiduels AI strategic-region, design IG, sémantique character/template, audit modifier, audit country-law, puis reindex/QA final.

- `ESTIMATED_PHASES_REMAINING_MIN = 5`
- `ESTIMATED_PHASES_REMAINING_LIKELY = 6`
- `ESTIMATED_PHASES_REMAINING_MAX = 8`

`NEXT_PHASE = LOG-CLEANUP-7-AI-LEGACY-STRATEGIC-REGION-RESIDUALS` n'est pas commencée.
