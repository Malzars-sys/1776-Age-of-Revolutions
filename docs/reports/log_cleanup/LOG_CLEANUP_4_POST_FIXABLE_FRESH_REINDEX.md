# LOG-CLEANUP-4 — Post-fixable fresh reindex

## Verdict

`LOG_CLEANUP_4 = PASS`

La génération humaine fraîche de LOG-CLEANUP-3 est encore physiquement présente et sa provenance correspond au rapport précédent. Le reparse complet produit une baseline courante de **327 identités** et **359 occurrences**. Aucun fichier gameplay n'a été modifié pendant cette phase.

Cette baseline est une photographie de la couverture réellement exercée entre 21:12:41 et 21:18:33. L'absence d'une famille runtime dans cette session ne prouve pas sa correction.

## Prévol et provenance

- branche : `post-2.3.0-log-cleanup`
- HEAD : `abaaad76b181a62c3673783c4bb74cdb3f1ee1b4`
- worktree avant LOG-CLEANUP-4 : propre
- index avant LOG-CLEANUP-4 : vide
- LOG-CLEANUP-3 : commit `abaaad7 Fix low-risk legacy script diagnostics`
- session locale : `2026-08-14 21:12:41` à `21:18:33` (`Europe/Paris`)
- version : `release/1.13.9 : afea32b87`
- The Great Wave : monté
- fork cible : monté
- autre build 1776 : non

Les hashes SHA-256 retenus sont :

| Segment | SHA-256 |
| --- | --- |
| `system.log` | `64E93779B7ECF93DA362555945A79229995C1D9DAD1CD25A535AFEB47635D612` |
| `debug.1.log` | `32915B69199FE2A86962FB24096F1609A9508E02AE2147B7E7E2E1B999DCA9C2` |
| `debug.log` | `7C2BA6CC194195D0BC7C7C65AAE1AE2D3D4C5DA113164307EFB17FDA0472A094` |
| `error.1.log` | `03322931ADCFF7ADACFB548F3BE79A06E404B14F6DD4A75118C653E4F2503DF9` |
| `error.log` | `5AB5B6341DE209392F2BA0755BF1A00F75C0155AD862608A9CA85DB0C1170195` |
| `game.log` | `C8FF41F055942E84F0F156B6438304E64D1961399293F9552B7AB78A0FCD08F1` |

Codex n'a pas lancé Victoria 3. Il a uniquement reparsé ces segments issus du runtime humain.

## Méthode de reparse

La taxonomie de LOG-CLEANUP-1 est conservée : `PARSER`, `POSTVALIDATE_TRIGGER`, `POSTVALIDATE_EFFECT`, `OTHER_ERROR`. Les warnings ne sont pas promus.

L'identité déterministe est formée par génération, message normalisé, chemin et ligne. Les enregistrements parseur multiligne contenant plusieurs messages ont été dépliés : chaque message et sa ligne interne deviennent une identité. Les répétitions exactes sont agrégées et leur nombre reste visible dans `count`.

Les familles `OTHER_ERROR` de LOG-CLEANUP-1 ont été recherchées dans `error.1.log` et `error.log`. Aucun `Invalid achievement`, aucun `not permitted to retain law`, et aucun des échecs de comparaison runtime précédemment indexés n'est présent dans cette session.

## Compteurs courants

| Compteur | Valeur |
| --- | ---: |
| identités totales | 327 |
| occurrences totales | 359 |
| parser | 117 |
| PostValidate total | 210 |
| PostValidate trigger | 188 |
| PostValidate effect | 22 |
| other error | 0 |
| chemins uniques | 72 |
| messages normalisés uniques | 65 |

Les 32 occurrences au-delà des 327 identités proviennent de répétitions `PostValidate`, principalement dans les segments rotatifs. Elles ne sont pas comptées comme de nouvelles identités.

## Comparaison avec LOG-CLEANUP-1

- identités exactes encore présentes : 307
- nouvelles identités : 20
- identités à ligne changée : 0
- identités LOG-CLEANUP-1 absentes de l'index frais : 251

Le compteur `DIAGNOSTICS_CLEARED_SINCE_LOG_CLEANUP_1 = 251` signifie ici **sorties de l'index courant par identité exacte**, pas « 251 corrections confirmées ». Il se décompose en 13 corrections confirmées par LOG-CLEANUP-2/3 et 238 diagnostics `OTHER_ERROR` non reproduits faute de couverture gameplay/registre externe dans cette session. Ces 238 ne sont donc pas déclarés corrigés.

Les 20 nouvelles identités sont : 18 messages d'API déjà couverts par des dispositions de chemin/famille ou nécessitant une décision sémantique, et 2 erreurs de variables de canton dans `common/flag_definitions/07_NM_Flags.txt`. Aucun changement de ligne ne peut être établi de façon univoque ; les deux nouveaux `has_port` aux lignes 358 et 360 sont de nouveaux emplacements, pas des déplacements des cinq emplacements historiques.

Les 13 diagnostics corrigés sont tous absents :

- `API_COUNTRY_CONVOYS_CAPACITY_MULT` : 0 régression sur 1 ;
- `LEGACY_LAW_ENACTMENT_MODIFIER` : 0 régression sur 11 ;
- `API_HAS_TECHNOLOGY_RESEARCHED` : 0 régression sur 1.

## Réévaluation des classifications

| Classification | Identités |
| --- | ---: |
| `FORK_ATTRIBUTABLE_FIXABLE` | 2 |
| `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | 46 |
| `UNKNOWN_REQUIRES_AUDIT` | 5 |
| `NEEDS_RUNTIME_REPRODUCTION` | 0 |
| `VANILLA_OR_EXTERNAL` | 54 |
| `ALREADY_ACCOUNTED_FOR` | 209 |
| `INTENTIONAL_FORK_DIVERGENCE` | 11 |
| **Somme** | **327** |

Chaque ligne de l'inventaire possède exactement une classification primaire.

Les 2 diagnostics fixables actuels appartiennent à `SYNTAX_FLAG_CANTON_SCALE_FILE_LOCAL_VARIABLES`. Le fichier fork-only `07_NM_Flags.txt` emploie à la ligne 186 deux variables définies dans un autre fichier de définitions ; le parseur les traite comme des tokens mal formés dans cette unité. La correction paraît bornée mais n'est pas appliquée ici.

### Dreyfus

Les deux identités `create_character` de `events/agitators_events/dreyfus_events.txt` sont reclassées de `FORK_ATTRIBUTABLE_FIXABLE` vers `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE`.

La preuve de LOG-CLEANUP-3 montre que les blocs d'événement ne sont pas la cause racine. `common/character_templates/dreyfus_template.txt` contient notamment `hq = region_france`, tandis que la forme vanilla 1.13.9 emploie une région HQ valide différente et des `home_region`. Le choix HQ/home region relève donc d'une décision sémantique de template. Aucun template n'a été modifié.

### Familles sémantiques actuelles

| Famille | Identités sémantiques |
| --- | ---: |
| `SYNTAX_STRATEGIC_REGION_LEGACY_KEYS` | 32 |
| `API_HAS_PORT` | 7 |
| `API_CREATE_CHARACTER` | 5 |
| `SYNTAX_INTEREST_GROUP_LEADER_CHANCE_KEYS` | 2 |
| **Total** | **46** |

Les cinq diagnostics `API_ADD_MODIFIER` / `API_ADD_ENACTMENT_MODIFIER` restent `UNKNOWN_REQUIRES_AUDIT`. La nouvelle occurrence confirme leur présence mais ne fournit pas de preuve suffisante pour choisir entre défaut du fork, contexte runtime incomplet ou comportement valide du moteur.

## Country law runtime

`COUNTRY_LAW_RUNTIME_DIAGNOSTICS_CURRENT = 0`.

La session retenue est une validation de chargement/menu et n'a pas reproduit les 113 identités `RUNTIME_COUNTRY_LAW_RETENTION` de LOG-CLEANUP-1. Elles ne sont ni divisées ni reclassées dans l'inventaire courant, car leur absence résulte d'une couverture gameplay insuffisante. Une reproduction humaine ciblée reste planifiée comme audit autonome ; aucune loi n'a été corrigée.

## Compteurs d'action

Les regroupements sont disjoints :

- `KNOWN_FORK_ERRORS_REQUIRING_CORRECTION = 48` = 2 fixables + 46 réécritures sémantiques ;
- `PENDING_ATTRIBUTION_OR_RUNTIME = 5` = 5 unknown actuels + 0 runtime actuel ;
- `NON_ACTIONABLE_OR_INTENTIONAL_RESIDUAL = 274` = 54 vanilla/external + 209 already accounted + 11 divergences intentionnelles.

`48 + 5 + 274 = 327`.

Le passif historique country-law non exercé est suivi dans la roadmap mais n'est pas ajouté artificiellement aux 327 identités courantes.

## Roadmap regroupée

La roadmap détaillée se trouve dans `LOG_CLEANUP_4_REMAINING_PHASE_PLAN.csv`. Le scénario probable compte sept phases :

1. correction bornée des deux tokens de canton ;
2. migration sémantique consolidée du fichier AI (`has_port` + régions stratégiques, 39 diagnostics) ;
3. décision sur les clés de chance de leader IG (2) ;
4. décision template/région pour les cinq `create_character`, incluant Dreyfus ;
5. audit d'attribution consolidé des cinq diagnostics modifier ;
6. reproduction gameplay ciblée des 113 country-law historiques non présents ici ;
7. reindex et QA runtime finaux.

Estimation : minimum 5, probable 7, maximum 9. Le minimum suppose le regroupement de familles de syntaxe compatibles et la consolidation des audits runtime. Le maximum couvre la séparation Dreyfus/Caucase et un lot correctif supplémentaire si l'audit modifier ou country-law attribue de nouvelles corrections au fork.

La prochaine phase sélectionnée est `LOG-CLEANUP-5-BOUNDED-FLAG-CANTON-PARSER-FIX`. Elle n'est pas commencée dans ce rapport.

## Livrables et validations

- `LOG_CLEANUP_4_DIAGNOSTIC_INVENTORY.csv` : 327 lignes, une par identité ;
- `LOG_CLEANUP_4_FAMILY_MATRIX.csv` : matrice famille × classification ;
- `LOG_CLEANUP_4_REMAINING_PHASE_PLAN.csv` : sept lots regroupés ;
- ce rapport.

Validations : unicité des identités, classification non vide et unique, somme des classifications égale à 327, somme A+B+C égale à 327, zéro régression des 13 diagnostics confirmés, `git diff --check`, portée documentaire uniquement, index Git laissé vide, aucun stage/commit/push.
