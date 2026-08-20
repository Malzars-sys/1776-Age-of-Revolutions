# LOG-CLEANUP-9 — Caucasus region and modifier API attribution

## État

LOG_CLEANUP_9 = PASS

STATIC_AUDIT = PASS

RUNTIME = PASS

Les sept identités initiales sont attribuées sans ambiguïté, les trois gates passent et le runtime humain frais ferme les sept diagnostics. Les huit substitutions appliquées correspondent à des homologues vanilla 1.13.9 exacts et ne produisent aucune nouvelle erreur attribuable.

## Upstream Tsar 2.3.0.1 audit

TSAR_UPSTREAM_VERSION_AUDITED = 2.3.0.1

GLOBAL_UPSTREAM_MERGE_REQUIRED = NO

UPSTREAM_TECHNICAL_FIX_REQUIRED = NO

L’audit comparatif Tsar est canonique et n’a pas été refait. Les overrides coloniaux BRZ/HAI/LOU/IQU, Count of Gálvez, les armées japonaises et la ligne vide européenne ne sont pas importés. Le diplomatic play Irak–Perse reste intact : sa suppression amont est un choix d’équilibrage hors LOG-CLEANUP-9.

## Prévol Git et baseline

- BRANCH = post-2.3.0-log-cleanup
- HEAD = d8cabd8bbe62dbe5c319d49aaa52ec7f0807c04f
- WORKTREE_INITIAL = CLEAN
- INDEX_INITIAL = EMPTY
- GAME_VERSION = release/1.13.9
- GAME_HASH = afea32b87
- VANILLA_ROOT = C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game
- KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 2
- UNKNOWN_REQUIRES_AUDIT_BEFORE = 5
- AUDIT_IDENTITIES_IN_SCOPE = 7

LOG-CLEANUP-8 est committé à HEAD. Les 113 diagnostics country-law, les eventtargetlinks globaux, le Tech Tree et toutes les familles interdites restent hors périmètre.

## Family A — Caucasus region legacy

CAUCASUS_REGION_MIGRATION_SAFE = YES

CAUCASUS_A1_OLD_EXPRESSION = region = sr:region_caucasus

CAUCASUS_A1_VANILLA_EXPRESSION = region = sr:region_russia

CAUCASUS_A2_OLD_EXPRESSION = region = sr:region_caucasus

CAUCASUS_A2_VANILLA_EXPRESSION = region = sr:region_russia

Les deux expressions appartiennent au country event caucasus_expulsions.1. La première filtre les states du pays contenant des pops circassiennes ; la seconde sélectionne aléatoirement un state avec les mêmes critères. L’homologue vanilla 1.13.9 conserve les scopes, la culture, la sélection et le sens géographique, mais utilise la région moderne sr:region_russia.

STATIC_REGION_CAUCASUS_REFERENCES_BEFORE = 3

Le sweep a trouvé une troisième référence dans caucasuswar.7 :

| Identité | Ancienne expression | Vanilla 1.13.9 | Décision |
|---|---|---|---|
| CAUCASUS-STATIC-01 | has_interest_marker_in_region = region_caucasus | has_interest_marker_in_region = sr:region_russia | Absorber dans la migration racine |
| CAUCASUS-A1 | region = sr:region_caucasus | region = sr:region_russia | Corriger |
| CAUCASUS-A2 | region = sr:region_caucasus | region = sr:region_russia | Corriger |

La référence latente a un homologue exact dans le même événement vanilla. Son patch ajoute aussi le namespace sr attendu par la signature moderne. Aucune autre référence region_caucasus ne reste dans le fichier.

- CAUCASUS_DIAGNOSTICS_BEFORE = 2
- CAUCASUS_CONFIRMED_DIAGNOSTICS_PATCHED = 2
- CAUCASUS_ROOT_CAUSE_STATIC_SWEEP_PATCHED = 1
- CAUCASUS_DIAGNOSTICS_AFTER = 0

## Family B — Morocco add_modifier

MOROCCO_ADD_MODIFIER_FIX_SAFE = YES

Les deux diagnostics se trouvent dans lands_of_anarchy.5, options A et B.

| Identité | Modifier | Scope | Cause racine | Homologue vanilla |
|---|---|---|---|---|
| MOROCCO-01 | lands_of_anarchy_tribe_recieved_medicine_mod | scope:anarchy_state_scope, type state | clé misspelled et absente | lands_of_anarchy_tribe_received_medicine_mod |
| MOROCCO-02 | lands_of_anarchy_tribe_recieved_medicine_mod | scope:anarchy_state_scope, type state | même faute de clé | lands_of_anarchy_tribe_received_medicine_mod |

MOROCCO_01_MODIFIER = lands_of_anarchy_tribe_received_medicine_mod

MOROCCO_01_SCOPE = state / scope:anarchy_state_scope

MOROCCO_01_ROOT_CAUSE = typo recieved; modifier inexistant

MOROCCO_02_MODIFIER = lands_of_anarchy_tribe_received_medicine_mod

MOROCCO_02_SCOPE = state / scope:anarchy_state_scope

MOROCCO_02_ROOT_CAUSE = typo recieved; modifier inexistant

Le modifier moderne existe dans common/static_modifiers/morocco_modifiers.txt et porte state_mortality_mult, ce qui confirme la compatibilité du scope state. La syntaxe add_modifier et les durées sont identiques à vanilla. Aucun autre changement de l’événement vanilla n’est importé.

- MOROCCO_DIAGNOSTICS_BEFORE = 2
- MOROCCO_UNKNOWN_DIAGNOSTICS_PATCHED = 2
- MOROCCO_DIAGNOSTICS_AFTER = 0

## Family C — Lobbies add_enactment_modifier

LOBBIES_ADD_ENACTMENT_MODIFIER_FIX_SAFE = YES

Les trois effets sont exécutés au ROOT d’un country event pendant une enactment active. Les événements sauvegardent actuellement_enacting_law dans scope:relevant_law_scope et leurs cancellation triggers protègent cette relation. La signature et le scope sont identiques à vanilla 1.13.9 ; seules les clés de modifier sont legacy.

| Identité | Event | Ancienne clé | Clé moderne définie | Cause racine |
|---|---|---|---|---|
| LOBBIES-01 | lobby_events.37.a | ig_law_enactment_time_good | ig_law_enactment_speed_good | migration time vers speed |
| LOBBIES-02 | lobby_events.38.b | ig_law_enactment_time_stall | ig_law_enactment_speed_stall | migration time vers speed |
| LOBBIES-03 | lobby_events.39.a | ig_law_enactment_time_good | ig_law_enactment_speed_good | migration time vers speed |

Les clés modernes sont définies dans vanilla common/static_modifiers/07_lobbies_03_modifiers.txt avec country_law_enactment_speed_mult à +0.15 ou -0.15. Les clés time_good/time_stall sont absentes de 1.13.9.

- LOBBIES_DIAGNOSTICS_BEFORE = 3
- LOBBIES_UNKNOWN_DIAGNOSTICS_PATCHED = 3
- LOBBIES_DIAGNOSTICS_AFTER = 0

## Attribution des cinq UNKNOWN

AUDIT_MATRIX_INITIAL_ROWS = 7

ROOT_CAUSE_STATIC_SWEEP_ROWS = 1

UNKNOWN_IDENTITIES_RESOLVED = 5

UNKNOWN_RECLASSIFIED_AS_FORK_ERROR = 5

UNKNOWN_RECLASSIFIED_AS_NON_ACTIONABLE = 0

UNKNOWN_REMAINING = 0

Les cinq identités passent de UNKNOWN_REQUIRES_AUDIT à FORK_ATTRIBUTABLE_FIXABLE. Aucune ne demande de réécriture sémantique, de décision gameplay ou de runtime ciblé séparé.

## Patch et empreintes

| Fichier gameplay | SHA256 avant | SHA256 après | Remplacements |
|---|---|---|---:|
| events/soi_events/00_ep1_caucasus_events.txt | 464EAEC89C265916D41CCAB66E6260CCD6995CFE860522D3FE34623D1C684EE5 | D297C1C9E3C4C5B5A39E2EB7DEA3BCA56DA059FCB5FE8C206CAF93E52401C4C4 | 3 |
| events/iberia_events/morocco_makhzen_events.txt | F0268C6EE8F0C2B3832BC099AA8205038FB83BE62F2EFD509AB41DE7301337C2 | DCF1B2C834850F26766780121E18F4DD5B881255CE3E7DEFD894DBA7681D780B | 2 |
| events/soi_events/00_lobbies_events_03.txt | ADE825D2F412E7E5849A43951CEAF1526B882508B352854C43EF9498BE0279AB | CF1AF70CD4FAA3D436EA4C2A6424C6D59170F8DBBA0F692732F802676E077AF9 | 3 |

- GAMEPLAY_CHANGED_FILES = 3
- GAMEPLAY_CHANGED_HUNKS = 6
- GAMEPLAY_INSERTIONS = 8
- GAMEPLAY_DELETIONS = 8
- DOCUMENTATION_FILES_CREATED = 2
- TECH_TREE_FILES_CHANGED = 0

## Validation statique

- git diff --check = PASS
- anciens region_caucasus dans le fichier Caucase = 0
- ancienne clé Morocco recieved = 0
- anciennes clés lobbies enactment_time_good/stall = 0
- nouvelles références sr:region_russia ciblées = 3
- nouvelle clé Morocco received ciblée = 2
- nouvelles clés lobbies enactment_speed_good/stall ciblées = 3
- fichiers gameplay modifiés hors allowlist = 0
- diplomatic play Irak–Perse modifié = NO
- Tech Tree modifié = NO
- staging, commit et push = NONE

## Runtime humain consolidé

Le runtime humain frais du 20 août 2026 couvre la session 17:33:20–17:40:55. Une nouvelle partie 1776 a été chargée avec les Pays-Bas et jouée environ une semaine.

Résultat fonctionnel :

- aucun crash ;
- aucune clé brute observée ;
- partie chargée et jouable ;
- fermeture normale avec Quit: Quit from inside game puis Transition Game->Empty.

Provenance :

- Victoria 3 = release/1.13.9 ;
- hash = afea32b87 ;
- code_revisions.log et system.log concordants.

Toutes les rotations error.5.log à error.log et game.5.log à game.log appartiennent à la session fraîche et ont été contrôlées, ainsi que debug.1.log, debug.log, dedicated_server.log, code_revisions.log et system.log.

| Log | SHA256 |
|---|---|
| code_revisions.log | 9C717EC653A786F236D848A3FFF5F14C262BBD38DBF0921896B5809C5DD75DDA |
| system.log | 5796953CF8AEA9908111158AFD247719826750328239F6A488451C083E525C86 |
| debug.1.log | D5D3FE21021D8145A8211F7BE72FC2B5AB222007BD607751F3EE0FC27FC10E35 |
| debug.log | 8EEC75AA999E273774201D8EBEF7B2C0310F5E8F9CF0E740AB768E2097D55687 |
| error.5.log | 4C9C7C90B047155D9EF7EB59270AF9F4896D7861A9A5EE4BD2FF2F5C715AC30D |
| error.4.log | E5BB5D698F996AD3E14727D406A6B1B750D1A5EDBDE725966581C140CAFCEDFA |
| error.3.log | 8C9E31FA65EE29FE714ABFE8A77777285BEA557AF960E1354122B7D8D10CFE6B |
| error.2.log | D9F65646E5E726D53CBE49D842B49A679C189000E03670B36A3D13EB6B62F283 |
| error.1.log | 3DC61DA4D8A3546774410BEFA31CF95B00824DAB2BF43DB0E3DB3D674CFBA4BF |
| error.log | 3931BCC1940DAD5E479125396C4C18E41DF3D9283876FA4176749CE2B07B5FFA |
| game.5.log | 294CAFD53BA1858402FE62FA33F646BCA235034217B334A3247A4119DC2E64DF |
| game.4.log | B4DD3C3D187B9A60E7F5206DE23358713ED2E00B9F50F35CFCA6D87E2FFE17D7 |
| game.3.log | 8C9E31FA65EE29FE714ABFE8A77777285BEA557AF960E1354122B7D8D10CFE6B |
| game.2.log | 9E88E6027E808B6FF3244A8CC9527804C31FED9FFCD42934E5CEB95A5DDA44E5 |
| game.1.log | 01C547644F54EE46EDE2875111BBB8D1E2733F1AF04F4B6B6E5CF6EC0C01F466 |
| game.log | 2675B941F5D589F4C6B4C6DD1FD2F7376A88745E226E694BA63BD394ED70726B |
| dedicated_server.log | 0F2774AB2FEABC5E5CA55B461E78DBC912AA7CAA3EC239E809AD747680484C80 |

Validation ciblée :

- CAUCASUS_DIAGNOSTICS_AFTER = 0
- MOROCCO_ADD_MODIFIER_DIAGNOSTICS_AFTER = 0
- LOBBIES_ADD_ENACTMENT_MODIFIER_DIAGNOSTICS_AFTER = 0
- NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0

## Nouvelles identités runtime hors périmètre

NEW_RUNTIME_IDENTITIES_PENDING_ATTRIBUTION = 8

Les rotations fraîches contiennent huit identités canonisées pour attribution ultérieure, avec manifestations croisées ou cascades associées. Elles comprennent notamment :

| Fichier | Lignes représentatives | Diagnostic |
|---|---|---|
| common/journal_entries/01_natural_borders_of_france.txt | 128, 129, 130 | Invalid right side during comparison 'sr' |
| common/scripted_buttons/00_new_colonial_admins.txt | 114, 553 | Invalid right side during comparison 'sr' |
| common/interest_groups/00_landowners.txt | 459 | has_law_or_variant trigger: Given law is a variant, we expect the parent |

Ces identités ne se trouvent dans aucun des trois hunks LOG-CLEANUP-9 et ne sont pas des régressions de la phase. Elles ne sont ni corrigées, ni ajoutées à NEW_CONFIRMED_FORK_ERRORS_DISCOVERED pendant cette finalisation. Leur attribution est intégrée au prochain audit country-law afin d’éviter une micro-phase séparée.

## Compteurs finaux

- UNKNOWN_IDENTITIES_RESOLVED = 5
- UNKNOWN_RECLASSIFIED_AS_FORK_ERROR = 5
- UNKNOWN_RECLASSIFIED_AS_NON_ACTIONABLE = 0
- UNKNOWN_REMAINING = 0
- KNOWN_CONFIRMED_ERRORS_CLEARED = 2
- NEW_CONFIRMED_FORK_ERRORS_DISCOVERED = 0
- NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0
- KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0
- HISTORICAL_COUNTRY_LAW_DIAGNOSTICS_REMAINING = 113

Calcul final : 2 - 2 + 5 + 0 - 5 = 0.

## Sortie finale

LOG_CLEANUP_9 = PASS

BRANCH = post-2.3.0-log-cleanup

HEAD = d8cabd8bbe62dbe5c319d49aaa52ec7f0807c04f

KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 2

UNKNOWN_REQUIRES_AUDIT_BEFORE = 5

AUDIT_IDENTITIES_IN_SCOPE = 7

CAUCASUS_REGION_MIGRATION_SAFE = YES

CAUCASUS_DIAGNOSTICS_BEFORE = 2

CAUCASUS_DIAGNOSTICS_PATCHED = 2

CAUCASUS_DIAGNOSTICS_AFTER = 0

MOROCCO_ADD_MODIFIER_FIX_SAFE = YES

MOROCCO_DIAGNOSTICS_BEFORE = 2

MOROCCO_DIAGNOSTICS_PATCHED = 2

MOROCCO_DIAGNOSTICS_AFTER = 0

LOBBIES_ADD_ENACTMENT_MODIFIER_FIX_SAFE = YES

LOBBIES_DIAGNOSTICS_BEFORE = 3

LOBBIES_DIAGNOSTICS_PATCHED = 3

LOBBIES_DIAGNOSTICS_AFTER = 0

UNKNOWN_IDENTITIES_RESOLVED = 5

UNKNOWN_RECLASSIFIED_AS_FORK_ERROR = 5

UNKNOWN_RECLASSIFIED_AS_NON_ACTIONABLE = 0

UNKNOWN_REMAINING = 0

KNOWN_CONFIRMED_ERRORS_CLEARED = 2

NEW_CONFIRMED_FORK_ERRORS_DISCOVERED = 0

NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0

KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0

NEW_RUNTIME_IDENTITIES_PENDING_ATTRIBUTION = 8

HISTORICAL_COUNTRY_LAW_DIAGNOSTICS_REMAINING = 113

GAMEPLAY_CHANGED_FILES = 3

GAMEPLAY_CHANGED_HUNKS = 6

DOCUMENTATION_FILES_CREATED = 2

TECH_TREE_FILES_CHANGED = 0

ESTIMATED_PHASES_REMAINING_MIN = 2

ESTIMATED_PHASES_REMAINING_LIKELY = 3

ESTIMATED_PHASES_REMAINING_MAX = 4

NEXT_PHASE = LOG-CLEANUP-10-RUNTIME-RESIDUALS-AND-COUNTRY-LAW-AUDIT

La phase suivante n’est pas commencée. Aucun git add, commit ou push n’a été effectué.
