# LOG-CLEANUP-8 — Character & leader semantic batch

## État

`STATIC_AUDIT = PASS`

`RUNTIME = PASS`

Les trois gates indépendantes passent. Le batch migre les deux anciennes probabilités de sélection du leader Landowners vers le système de poids 1.13.9, corrige les dépendances structurales Dreyfus/Esterhazy et remplace les trois HQ Caucase invalides sans modifier les biographies du fork.

## Prévol Git

- branche : `post-2.3.0-log-cleanup` ;
- HEAD : `820b1c263a521491efa0e3581299db5dbee831fd` ;
- commit HEAD : `820b1c2 Migrate residual legacy AI strategic regions` ;
- worktree initial : propre ;
- index initial : vide ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 7`.

## Identités d'entrée

Le runtime frais LOG-CLEANUP-7 reproduit exactement les sept identités :

- `Unexpected token: commander_leader_chance` — `common/interest_groups/00_landowners.txt:707` ;
- `Unexpected token: executive_leader_chance` — `common/interest_groups/00_landowners.txt:714` ;
- `PostValidate of effect 'create_character' returned false` — `events/agitators_events/dreyfus_events.txt:84` ;
- même message — `events/agitators_events/dreyfus_events.txt:244` ;
- même message — `events/soi_events/00_ep1_caucasus_events.txt:730` ;
- même message — `events/soi_events/00_ep1_caucasus_events.txt:759` ;
- même message — `events/soi_events/00_ep1_caucasus_events.txt:1039`.

La matrice `LOG_CLEANUP_8_SEMANTIC_DECISION_MATRIX.csv` contient exactement une ligne par identité, soit sept lignes.

## Family A — Interest Group leader semantics

`IG_SEMANTIC_MIGRATION = YES`

- `OLD_SYSTEM = probability that the most popular commander or executive takes over when leadership changes` ;
- `NEW_SYSTEM = candidate-pool weights for appropriate commander, magnate and executive candidates` ;
- `MIGRATION_RATIONALE = the legacy block is unchanged since initial import and matches an obsolete vanilla system; its script-value multiplier no longer exists anywhere in 1.13.9` ;
- `VALUES_SELECTED = commander 1.5; magnate 5.0 plus 5 before the Japanese restoration; executive 0.5` ;
- `VANILLA_RELATION = exact complete Landowners leader-weight block from vanilla 1.13.9` ;
- `FORK_INTENT_PRESERVED = YES_AS_OFFICIAL_LANDOWNERS_BEHAVIOR, not as a false numeric probability equivalence`.

Le simple renommage rejeté par LOG-CLEANUP-5 n'est pas utilisé. Les anciennes valeurs `0.5` et `0.1` appartenaient à des probabilités et ne sont pas recopiées dans des poids. Le bloc moderne complet est nécessaire pour ne pas omettre les magnates ni la règle japonaise. Il conserve l'intention générale d'un Landowners favorisant les candidats issus des élites foncières et militaires, tout en adoptant l'algorithme réellement compris par 1.13.9.

Historique Git : les douze lignes legacy viennent toutes du commit d'import initial `b602804`; `git blame` et `git log -S` ne montrent aucune divergence volontaire ultérieure du fork.

- `IG_DIAGNOSTICS_BEFORE = 2`
- `IG_DIAGNOSTICS_PATCHED = 2`
- anciennes clés et multiplicateur legacy après patch : 0

## Family B1 — Dreyfus templates

`DREYFUS_TEMPLATE_MIGRATION_SAFE = YES`

Les deux appels `create_character` des events sont déjà homologues à vanilla et restent inchangés. La dépendance responsable est :

- `DEPENDENCY_FILE = common/character_templates/dreyfus_template.txt` ;
- `DEPENDENCY_REASON = two referenced templates contain invalid hq = region_france and lack the modern home_region fields` ;
- `DIAGNOSTICS_AFFECTED = DREYFUS-01, DREYFUS-02`.

| Personnage | Ancien HQ | HQ vanilla 1.13.9 | Home region | Rôle | Culture | Religion | Idéologie | Autres différences ciblées |
|---|---|---|---|---|---|---|---|---|
| Alfred Dreyfus | `region_france` | `region_western_europe` | `STATE_ALSACE_LORRAINE` | general | `cu:ashkenazi` | `rel:jewish` | `ideology_moderate` | aucune après ajout des deux champs structuraux |
| Ferdinand Walsin Esterhazy | `region_france` | `region_western_europe` | `STATE_ILE_DE_FRANCE` | general | `cu:french` | `rel:catholic` | `ideology_moderate` | aucune après ajout des deux champs structuraux |

Les noms, dates, cultures, religions, idéologies, traits, rôles et rangs ne changent pas. Le template Zola n'est pas une dépendance des deux diagnostics et reste inchangé, y compris son absence de `home_region` dans le fork.

- `DREYFUS_DIAGNOSTICS_BEFORE = 2`
- `DREYFUS_DIAGNOSTICS_PATCHED = 2`
- `events/agitators_events/dreyfus_events.txt` modifié : NO

## Family B2 — Caucasus characters

`CAUCASUS_CHARACTER_MIGRATION = YES`

Les rotations fraîches donnent le message complet générique `PostValidate of effect 'create_character' returned false` pour les lignes 730, 759 et 1039 ; aucune continuation plus détaillée n'est émise dans `debug.1.log`, `debug.log`, les six rotations `error` ou les six rotations `game`. L'attribution est néanmoins directe : chaque bloc contient `hq = region_caucasus`, objet HQ absent en 1.13.9, et chaque homologue vanilla utilise une template avec `hq = region_russia`.

| Diagnostic | Event | Personnage | Template vanilla de preuve | Cause racine | Structure vanilla | Décision | Patché |
|---|---|---|---|---|---|---|---|
| CAUCASUS-01 | `caucasuswar.7.a` | Qerandiqo Berzeg | `CIR_qerandiqo_berzeg` | HQ legacy `region_caucasus` | HQ `region_russia`, home `STATE_KUBAN` | remplacer uniquement le HQ inline | YES |
| CAUCASUS-02 | `caucasuswar.7.b` | Qerandiqo Berzeg | `CIR_qerandiqo_berzeg` | HQ legacy `region_caucasus` | HQ `region_russia`, home `STATE_KUBAN` | remplacer uniquement le HQ inline | YES |
| CAUCASUS-03 | `caucasuswar.10.a` | Teofil Lapinski | `CIR_teofil_lapinski` | HQ legacy `region_caucasus` | HQ `region_russia`, home `STATE_WEST_GALICIA` | remplacer uniquement le HQ inline | YES |

Le fichier vanilla `common/character_templates/country_chc.txt` est une preuve en lecture seule, pas une dépendance modifiée. Garder les personnages inline évite d'importer une template entière et préserve toutes les particularités du fork. En particulier, l'idéologie `ideology_radical` de Łapiński reste inchangée malgré `ideology_republican_leader` dans la template vanilla.

- `DEPENDENCY_FILE = C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\common\character_templates\country_chc.txt (READ_ONLY_PROOF)` ;
- `DEPENDENCY_REASON = contains the exact 1.13.9 Qerandiqo and Lapinski structural homologs` ;
- `DIAGNOSTICS_AFFECTED = CAUCASUS-01, CAUCASUS-02, CAUCASUS-03` ;
- `CAUCASUS_DIAGNOSTICS_BEFORE = 3` ;
- `CAUCASUS_DIAGNOSTICS_PATCHED = 3`.

Le diagnostic distinct `has_interest_marker_in_region` à la ligne 783 est déjà classé et reste hors périmètre ; aucune autre ligne du fichier Caucase n'est modifiée.

## Patch et empreintes

| Fichier modifié | SHA-256 avant | SHA-256 après |
|---|---|---|
| `common/interest_groups/00_landowners.txt` | `F209C8E9DC3C0DCA6D30EB3312CED08C779C5C394935E23BFE2B145F82C2FFC4` | `E0A4473DC85842382CC0F34088EDE4C07575BBF96BB87E78E68E3189FFE29B5C` |
| `common/character_templates/dreyfus_template.txt` | `14B5A98B0FDEA0B61EE6A47BA600AE97A83E23D834EDF2AE03384378E86771E4` | `0EA083F87B5C2D70251DEC38A921A5A7827695CD14B7988B4359CE5B60ACD5AA` |
| `events/soi_events/00_ep1_caucasus_events.txt` | `F905C81D95AF6788CE358CB607C7AD5845A83D1A6D005AF9053BB2194FF0691F` | `464EAEC89C265916D41CCAB66E6260CCD6995CFE860522D3FE34623D1C684EE5` |

- `TOTAL_KNOWN_DIAGNOSTICS_PATCHED = 7`
- `GAMEPLAY_CHANGED_FILES = 3`
- `GAMEPLAY_CHANGED_HUNKS = 9`
- `GAMEPLAY_INSERTIONS = 30`
- `GAMEPLAY_DELETIONS = 14`

## Validation statique

- `git diff --check` : PASS ;
- anciennes clés leader et multiplicateur obsolète : 0 ;
- `hq = region_france` dans la template ciblée : 0 ;
- `hq = region_caucasus` dans les trois blocs ciblés : 0 ;
- `region_western_europe`, `region_russia`, `STATE_ALSACE_LORRAINE` et `STATE_ILE_DE_FRANCE` : définis physiquement en vanilla 1.13.9 ;
- accolades : Landowners 245/245, Dreyfus 6/6, Caucase 648/648 ;
- fichier AI LOG-CLEANUP-6/7 : inchangé ;
- fichier Tech Tree : inchangé ;
- index Git : vide ;
- staging/commit/push : aucun.

## Runtime humain consolidé

Le runtime humain frais du 14 août 2026 couvre la session `23:44:40–23:48:10`, atteint le menu principal et se termine proprement avec `Quit: Quit from inside game` puis `Transition Game->Empty`. `system.log` confirme `release/1.13.9 : afea32b87`; `debug.1.log` confirme le montage unique du fork `1776_Age_of_Revolutions_fork` et du mod `Age of revolution /Fork`.

Rotations appartenant à la session et analysées :

| Log | SHA-256 |
|---|---|
| `debug.1.log` | `B15858C540F404C2755A3381F2E885A851109958F0BAFF1F6D32989597E29008` |
| `debug.log` | `98E3868F26EA20B3F9CDA061807E5D90ECF23C284569D965B8F2AA3AFB134784` |
| `error.log` | `5B538D2343F552B1F548EDC49329A15EC620E734A9A62D6FDB4EB3BC06E1EF62` |
| `game.log` | `43F6A528E00A2E96E1B5EE4F7C3D8652E5D590A239BF4ED0640593580F5DBA41` |
| `code_revisions.log` | `34B21593068EDF59D75A9216572C0D8D1AAB4387E36BE8242FB2346A19842F0B` |
| `system.log` | `19AF0168163EEC997887F71C2CFBF5A211E8364082B106397D06FE63D1FCEBE1` |
| `dedicated_server.log` | `2F8BF36012B0866E155C5D2D8C26F0A4DA111B45FA3B39CBA288096567A7C521` |

Les rotations numérotées `error.*` et `game.*` sont antérieures à `23:44:40` et ne sont pas mélangées à cette mesure. Les sept identités ciblées sont absentes de tous les segments frais :

- `IG_DIAGNOSTICS_AFTER = 0` ;
- `DREYFUS_DIAGNOSTICS_AFTER = 0` ;
- `CAUCASUS_DIAGNOSTICS_AFTER = 0` ;
- `KNOWN_ERRORS_CLEARED = 7` ;
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0`.

## Nouvelles identités découvertes hors patch

Selon la méthode des batches LOG-CLEANUP-6/7, le compteur de découverte ciblé retient les nouvelles identités situées dans les fichiers gameplay modifiés par la phase. Le runtime a révélé deux identités `Invalid database object key 'region_caucasus'` supplémentaires dans le fichier Caucase modifié, sans rapport avec les trois blocs `create_character` du patch :

| Fichier | Ligne | Contexte | Attribution |
|---|---:|---|---|
| `events/soi_events/00_ep1_caucasus_events.txt` | 1982 | trigger de `caucasus_expulsions.1` | ligne non touchée par le patch ; vanilla 1.13.9 emploie `region_russia` dans l'homologue |
| `events/soi_events/00_ep1_caucasus_events.txt` | 1995 | sélection d'état de `caucasus_expulsions.1` | ligne non touchée par le patch ; vanilla 1.13.9 emploie `region_russia` dans l'homologue |

`error.log` porte une occurrence de chacune à `23:47:33`; leur miroir dans `game.log` n'est pas compté comme une identité supplémentaire. Le diff prouve que les deux lignes sont en dehors des trois blocs `create_character` corrigés. Elles sont donc confirmées comme erreurs préexistantes du fork et non comme régressions attribuables au patch.

La session émet également un ensemble global d'`eventtargetlinks` dans des fichiers hors périmètre. Comme dans les phases ciblées précédentes, ces émissions ne sont pas promues individuellement dans le compteur opérationnel de ce batch : elles demandent le fresh global reindex prévu par la roadmap, avec déduplication contre les familles legacy et country-law déjà classées.

- `NEW_CONFIRMED_FORK_ERRORS_DISCOVERED = 2` ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 7 - 7 + 2 = 2` ;
- `UNKNOWN_REQUIRES_AUDIT_REMAINING = 5` ;
- `HISTORICAL_COUNTRY_LAW_DIAGNOSTICS_REMAINING = 113`.

## Conclusion et suite

`LOG_CLEANUP_8 = PASS` : les trois gates passent, les sept erreurs ciblées sont fermées et aucune nouvelle erreur n'est attribuable au patch. Le compteur opérationnel ciblé ne peut toutefois pas être forcé à zéro en raison des deux références Caucase nouvellement confirmées dans le fichier audité.

- `ESTIMATED_PHASES_REMAINING_MIN = 3` ;
- `ESTIMATED_PHASES_REMAINING_LIKELY = 4` ;
- `ESTIMATED_PHASES_REMAINING_MAX = 6` ;
- `NEXT_PHASE = LOG-CLEANUP-9-CAUCASUS-REGION-AND-MODIFIER-API-ATTRIBUTION-AUDIT`.

La phase suivante n'est pas commencée. Aucun staging, commit ou push n'a été effectué.
